# Network Traffic Anomaly Detector

A safe offline analyzer for CSV network-flow exports. It does not capture packets or scan hosts.

## CSV format
`timestamp,src_ip,dst_ip,dst_port,bytes,protocol`

## Run
```bash
python traffic_detector.py sample_flows.csv --ports-threshold 10
```

The detector flags source IPs contacting many distinct destination ports and unusually high byte totals. Tune thresholds for your environment.
