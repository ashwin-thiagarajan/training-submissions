class ResponseJson:
    @staticmethod
    def response_json_object(service_name, time_taken, status_code, status, output):
        return {
            "message": service_name,
            "status": status,
            "statusCode": status_code,
            "respTime": int(time_taken * 1000),
            "output": output,
        }
