from .prometheus_exporter import PrometheusExporter


def main():
    exporter = PrometheusExporter()
    exporter.run()


if __name__ == "__main__":
    main()
