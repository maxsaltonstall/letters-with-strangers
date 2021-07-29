#!/bin/bash
# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Install and start the Google logging agent (google-fluentd).
#
# Usage: sudo bash install-logging-agent.sh [ --structured | --unstructured ]
#
# This script does the following:
#
#   1. Configures the required apt or yum repository.
#      The environment variable REPO_SUFFIX can be set to alter which
#      repository is used.  A dash (-) will be inserted prior to the supplied
#      suffix. Example values are 'unstable' or '20151027-1'.
#   2. Installs the logging agent.
#   3. Unless the DO_NOT_INSTALL_CATCH_ALL_CONFIG environment variable is set:
#      1. Installs "catch-all" configuration files.
#      2. Restarts the logging agent, to pick up the new configuration files.
#      3. Sends a test message to syslog which should be visible in the log
#         viewer.
#
# Ignore the return code of command substitution in variables.
# shellcheck disable=SC2155

# TODO(lingshi): Add "set -e".

# Name of the logging agent.
AGENT_NAME='google-fluentd'

# Default name of the config files package. Overridden in main().
# We currently default to the unstructured version of the config. Please note,
# the default behavior may change in the future. If you would like guaranteed
# behavior, please pass --unstructured or --structured explicitly.
CONFIG_NAME='google-fluentd-catch-all-config'

# Host that serves the repositories.
REPO_HOST='packages.cloud.google.com'

# URL for the logging agent documentation.
LOGGING_AGENT_DOCS_URL="https://cloud.google.com/logging/docs/agent"

# URL documentation which lists supported platforms for running the logging agent.
LOGGING_AGENT_SUPPORTED_URL="${LOGGING_AGENT_DOCS_URL}/#agent-os-list"

install_catch_all_config="true"
if [[ -n "${DO_NOT_INSTALL_CATCH_ALL_CONFIG}" ]]; then
  install_catch_all_config="false"
fi

# Recent systems provide /etc/os-release. The ID variable defined therein
# is particularly useful for identifying Amazon Linux.
if [[ -f /etc/os-release ]]; then
  . /etc/os-release
fi

preinstall() {
  cat <<EOM
==============================================================================
Starting installation of ${AGENT_NAME}
==============================================================================

EOM
}

postinstall() {
  exit_code=0

  restart_exit_code=0
  if [[ "${install_catch_all_config}" == "true" ]]; then
    service ${AGENT_NAME} restart
    restart_exit_code=$?

    logger "Test syslog message from ${AGENT_NAME}-${VERSION} at $(date)."
  fi

  if [[ $restart_exit_code -eq 0 ]]; then
    fluentd_log="/var/log/${AGENT_NAME}/${AGENT_NAME}.log"
    logs_viewer_url=$(grep 'Logs viewer address: ' ${fluentd_log} | tail -1 |\
      sed -e 's/.*Logs viewer address: //')
    if [[ -z "$logs_viewer_url" ]]; then
      logs_viewer_url="(failed to obtain logs viewer URL from agent log)"
    fi

    cat <<EOM

==============================================================================
Installation of ${AGENT_NAME} complete.

Logs from this machine should be visible in the log viewer at:
  ${logs_viewer_url}

A test message has been sent to syslog to help verify proper operation.

Please consult the documentation for troubleshooting advice:
  ${LOGGING_AGENT_DOCS_URL}

You can monitor the logging agent's logfile at:
  ${fluentd_log}
==============================================================================
EOM

    # Prints an additional banner if we appear to have a credentials issue.
    check_credentials
  else
    cat <<EOM

==============================================================================
Errors occurred while installing ${AGENT_NAME}-${VERSION}. See the log snippet
above or run:
  sudo service ${AGENT_NAME} status
==============================================================================
EOM
    exit_code=1
  fi

  return "$exit_code"
}

install_for_debian() {
  lsb_release -v >/dev/null 2>&1 || { \
    apt-get update && apt-get -y install lsb-release; \
  }
  local CODENAME="${REPO_CODENAME:-"$(lsb_release -sc)"}"
  local REPO_NAME="google-cloud-logging-${CODENAME}${REPO_SUFFIX+-${REPO_SUFFIX}}"
  cat > /etc/apt/sources.list.d/google-cloud-logging.list <<EOM
deb http://${REPO_HOST}/apt ${REPO_NAME} main
EOM
  curl -s -f https://${REPO_HOST}/apt/doc/apt-key.gpg | apt-key add -
  apt-get update \
    -o Dir::Etc::sourcelist="sources.list.d/google-cloud-logging.list" \
    -o Dir::Etc::sourceparts="-" -o APT::Get::List-Cleanup="0"
  local -a PACKAGES=("${AGENT_NAME}")
  if [[ "${install_catch_all_config}" == "true" ]]; then
    PACKAGES+=("${CONFIG_NAME}")
  fi
  DEBIAN_FRONTEND=noninteractive apt-get -y install "${PACKAGES[@]}"
  VERSION="$(dpkg -l google-fluentd | tail -n 1 |\
    sed -E 's/.*([0-9]+\.[0-9]+\.[0-9]+-[0-9]+).*/\1/')"
}

# takes the repo name as a parameter
install_rpm() {
  lsb_release -v >/dev/null 2>&1 || yum -y install redhat-lsb-core
  local REPO_NAME="${1}${REPO_SUFFIX+-${REPO_SUFFIX}}"
  cat > /etc/yum.repos.d/google-cloud-logging.repo <<EOM
[google-cloud-logging]
name=Google Cloud Logging Agent Repository
baseurl=https://${REPO_HOST}/yum/repos/${REPO_NAME}
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://${REPO_HOST}/yum/doc/yum-key.gpg
       https://${REPO_HOST}/yum/doc/rpm-package-key.gpg
EOM
  local -a PACKAGES=("${AGENT_NAME}")
  if [[ "${install_catch_all_config}" == "true" ]]; then
    PACKAGES+=("${CONFIG_NAME}")
  fi
  yum -y install "${PACKAGES[@]}"
  VERSION="$(yum list google-fluentd.x86_64 | tail -n 1 |\
    sed -E 's/.*([0-9]+\.[0-9]+\.[0-9]+-[0-9]+).*/\1/')"
}

install_for_redhat() {
  local VERSION_PRINTER='import platform; print(platform.dist()[1].split(".")[0])'
  local MAJOR_VERSION="$(python2 -c "${VERSION_PRINTER}")"
  local REPO_NAME="google-cloud-logging-el${MAJOR_VERSION}-\$basearch"
  install_rpm "${REPO_NAME}"
  exit_code=$?
  service "${AGENT_NAME}" start || true
  return "$exit_code"
}

install_for_amazon_linux() {
  local REPO_NAME="google-cloud-logging-el6-\$basearch"
  install_rpm "${REPO_NAME}"
  exit_code=$?
  service "${AGENT_NAME}" start || true
  return "$exit_code"
}

install_for_suse() {
  SUSE_VERSION=${VERSION%%-*}
  local REPO_NAME="google-cloud-logging-sles${SUSE_VERSION}-\$basearch${REPO_SUFFIX+-${REPO_SUFFIX}}"
  # TODO: expand all short arguments in this script, for readability.
  zypper -n refresh || { \
    echo "Could not refresh zypper repositories."; \
    echo "This is not necessarily a fatal error; proceeding..."; \
  }
  zypper addrepo -g -t YUM "https://${REPO_HOST}/yum/repos/${REPO_NAME}" google-cloud-logging
  rpm --import "https://${REPO_HOST}/yum/doc/yum-key.gpg" "https://${REPO_HOST}/yum/doc/rpm-package-key.gpg"
  zypper -n refresh google-cloud-logging || { \
    echo "Could not refresh the Stackdriver agent zypper repositories."; \
    echo "Please check your network connectivity and"; \
    echo "make sure you are running a supported SUSE distribution."; \
    echo "See ${LOGGING_AGENT_SUPPORTED_URL} for a list of supported platforms."; \
    exit 1; \
  }
  local -a PACKAGES=("${AGENT_NAME}")
  if [[ "${install_catch_all_config}" == "true" ]]; then
    PACKAGES+=("${CONFIG_NAME}")
  fi
  zypper -n install -y "${PACKAGES[@]}"
  systemctl daemon-reload

  VERSION="$(rpm -qa "${AGENT_NAME}" | tail -n 1 |\
    sed -E 's/.*([0-9]+\.[0-9]+\.[0-9]+-[0-9]+).*/\1/')"
}

check_credentials() {
  if curl --connect-timeout 2 -s -i http://169.254.169.254 | \
      grep -i '^Metadata-Flavor: Google' > /dev/null 2>&1; then
    # running on GCP; we can get credentials from the built-in service account.
    return
  fi

  # Check for GOOGLE_APPLICATION_CREDENTIALS, which might be set in
  # /etc/sysconfig or /etc/default.
  [[ -f "/etc/sysconfig/${AGENT_NAME}" ]] && source "/etc/sysconfig/${AGENT_NAME}"
  [[ -f "/etc/default/${AGENT_NAME}" ]] && source "/etc/default/${AGENT_NAME}"
  if [[ -n "$GOOGLE_APPLICATION_CREDENTIALS" && \
        -f "$GOOGLE_APPLICATION_CREDENTIALS" ]]; then
    return
  fi

  # Look at the user and system default paths.
  for path in /root/.config/gcloud/application_default_credentials.json \
      /etc/google/auth/application_default_credentials.json; do
    if [[ -f "$path" ]]; then
      return
    fi
  done

  cat <<EOM

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: Google Compute Platform credentials are required for this platform
but were not found, thus the agent may have failed to start or initialize
properly.  Please consult the "Authorization" section of the documentation at
${LOGGING_AGENT_DOCS_URL} then restart the agent using:

  sudo service ${AGENT_NAME} restart
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

EOM
}

install() {
  case "${ID:-}" in
    amzn)
      echo 'Installing agent for Amazon Linux.'
      install_for_amazon_linux
      ;;
    debian|ubuntu)
      echo 'Installing agent for Debian or Ubuntu.'
      install_for_debian
      ;;
    rhel|centos)
      echo 'Installing agent for RHEL or CentOS.'
      install_for_redhat
      ;;
    sles)
      echo 'Installing agent for SLES.'
      install_for_suse
      ;;
    *)
      # Fallback for systems lacking /etc/os-release.
      if [[ -f /etc/debian_version ]]; then
        echo 'Installing agent for Debian.'
        install_for_debian
      elif [[ -f /etc/redhat-release ]]; then
        echo 'Installing agent for Red Hat.'
        install_for_redhat
      elif [[ -f /etc/SuSE-release ]]; then
        echo 'Installing agent for SLES.'
        install_for_suse
      else
        echo >&2 'Unidentifiable or unsupported platform.'
        exit 1
      fi
  esac
}

main() {
  case $1 in
    --structured)
      CONFIG_NAME='google-fluentd-catch-all-config-structured'
      ;;
    --unstructured)
      CONFIG_NAME='google-fluentd-catch-all-config'
      ;;
  esac

  preinstall

  if ! install; then
    echo >&2 'Installation failed.'
    exit 1
  fi

  postinstall
  return $?
}

main "$@"
