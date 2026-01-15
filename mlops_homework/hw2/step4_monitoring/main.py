from src.monitor import monitor_health, monitor_predict, get_alert_level
from src.config import load_config
from src.logger import print_alert
from src.logger import JSONLogger
import time

def calc_p95(latencies):
    if not latencies:
        return None
    sorted_lat = sorted(latencies)
    k = int(len(latencies)*0.95)
    return sorted_lat[min(k, len(sorted_lat)-1)]

def calc_error_rate(status_codes):
    errors = sum(1 for code in status_codes if code is None or code >= 400)
    return errors / len(status_codes) if status_codes else None

def calc_consecutive_failures(status_codes):
    count = 0
    for code in reversed(status_codes):
        if code is None or code >= 400:
            count += 1
        else:
            break
    return count

def main():
    api_url = "localhost:8000"
    image_path = "test_images/img.jpg"
    iterations = 5

    latencies_health, codes_health = [], []
    latencies_predict, codes_predict = [], []

    logger = JSONLogger()
    logger.log("INFO", "Запуск мониторинга", api_url=api_url, image_path=image_path, iterations=iterations)

    for i in range(iterations):
        logger.log("INFO", "Начало итерации мониторинга", iteration=i)
        try:
            # Health мониторинг
            health = monitor_health(api_url)
            print("health:", health)
            latencies_health.append(health["latency"])
            codes_health.append(health["status_code"])

            # Predict мониторинг (одна картинка)
            predict = monitor_predict(api_url, image_path)
            print("predict:", predict)
            latencies_predict.append(predict["latency"])
            codes_predict.append(predict["status_code"])

            time.sleep(1)
        except Exception as e:
            logger.log("ERROR", "Ошибка в процессе мониторинга", iteration=i, error=str(e))

    # Расчет метрик
    p95_health = calc_p95(latencies_health)
    error_rate_health = calc_error_rate(codes_health)
    consecutive_failures_health = calc_consecutive_failures(codes_health)

    p95_predict = calc_p95(latencies_predict)
    error_rate_predict = calc_error_rate(codes_predict)
    consecutive_failures_predict = calc_consecutive_failures(codes_predict)

    # Логирование метрик в отдельный файл
    logger.log_metric("p95_latency_health", p95_health)
    logger.log_metric("error_rate_health", error_rate_health)
    logger.log_metric("consecutive_failures_health", consecutive_failures_health)

    logger.log_metric("p95_latency_predict", p95_predict)
    logger.log_metric("error_rate_predict", error_rate_predict)
    logger.log_metric("consecutive_failures_predict", consecutive_failures_predict)

    print("\n--- /health метрики ---")
    print("P95 latency:", calc_p95(latencies_health))
    print("Error rate:", calc_error_rate(codes_health))
    print("Consecutive failures:", calc_consecutive_failures(codes_health))

    print("\n--- /predict метрики ---")
    print("P95 latency:", calc_p95(latencies_predict))
    print("Error rate:", calc_error_rate(codes_predict))
    print("Consecutive failures:", calc_consecutive_failures(codes_predict))

    color_monitor = {
        'response_time_ms': latencies_predict,
        'p95_latency_ms': calc_p95(latencies_predict),
        'error_rate_percent': calc_error_rate(codes_predict),
        'consecutive_failures': calc_consecutive_failures(codes_predict),
    }

    config = load_config("config\monitoring_config.yaml")

    # Warning пороги
    response_time_warning = config["thresholds"]["response_time_ms"]["warning"]
    latency_warning = config["thresholds"]["p95_latency_ms"]["warning"]
    error_warning = config["thresholds"]["error_rate_percent"]["warning"]
    failures_warning = config["thresholds"]["consecutive_failures"]["warning"]

    # Crititcal пороги
    response_time_critical = config["thresholds"]["response_time_ms"]["critical"]
    latency_critical = config["thresholds"]["p95_latency_ms"]["critical"]
    error_critical = config["thresholds"]["error_rate_percent"]["critical"]
    failures_critical = config["thresholds"]["consecutive_failures"]["critical"]

    for i in color_monitor['response_time_ms']:
        print('\n----Время отклика----')
        print_alert(f'{i}', get_alert_level(i, response_time_warning, response_time_critical))
    
    print('\n--P95--')
    print_alert(f'{color_monitor.get("p95_latency_ms")}', get_alert_level(color_monitor.get('p95_latency_ms'), latency_warning, latency_critical))

    print('\n--Error rate--')
    print_alert(f'{color_monitor.get("error_rate_percent")}', get_alert_level(color_monitor.get('error_rate_percent'), error_warning, error_critical))

    print('\n--Consecutive failures--')
    print_alert(f'{color_monitor.get("consecutive_failures")}', get_alert_level(color_monitor.get('consecutive_failures'), failures_warning, failures_critical))

if __name__ == "__main__":
    main()