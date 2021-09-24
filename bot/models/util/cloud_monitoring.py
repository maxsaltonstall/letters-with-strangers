from ... import config

import time, logging, requests

from google.cloud import monitoring_v3


def emit_float_metric(metric_series: str, metric_value: float):
    
    logging.debug(f"Cloud Monitoring enabled: {config.cloud_monitoring_enabled}")
    
    if config.cloud_monitoring_enabled:
        try:
            # retrieve instance metadata from metadata server
            project_id = requests.get("http://metadata/computeMetadata/v1/project/project-id",
                                      headers={'Metadata-Flavor': 'Google'}).text
            instance_id = requests.get("http://metadata/computeMetadata/v1/instance/id",
                                       headers={'Metadata-Flavor': 'Google'}).text
            zone = requests.get("http://metadata/computeMetadata/v1/instance/zone",
                                headers={'Metadata-Flavor': 'Google'}).text.split("/")[-1]

            logging.debug(f"project_id = {project_id}")
            logging.debug(f"instance_id = {instance_id}")
            logging.debug(f"zone = {zone}")

            monitoring_client = monitoring_v3.MetricServiceClient()
            
            project_name = f"projects/{project_id}"

            series = monitoring_v3.TimeSeries()
            series.resource.type = "gce_instance"
            series.resource.labels["instance_id"] = instance_id
            series.resource.labels["zone"] = zone

            series.metric.type = f"custom.googleapis.com/{metric_series}"

            now = time.time()
            seconds = int(now)
            nanos = int((now - seconds) * 10 ** 9)
            interval = monitoring_v3.TimeInterval(
                {"end_time": {"seconds": seconds, "nanos": nanos}}
            )
            point = monitoring_v3.Point({"interval": interval, "value": {"double_value": metric_value}})
            series.points = [point]
            monitoring_client.create_time_series(request={"name": project_name, "time_series": [series]})
        except Exception as e:
            logging.error(f"Unable to emit metric [series: {metric_series}; value: {metric_value}]")
            logging.error(str(e))
    else:
        logging.info(f"Cloud Monitoring is disabled; falling back to logging [series: {metric_series}; value: {metric_value}]")
