import json


class Controller(object):
    def format_response(self, response):
        if isinstance(response, str):
            return response
        elif isinstance(response, dict) or isinstance(response, list):
            return json.dumps(response)

    def create_response(self, service_result, cases):
        code, result = service_result
        # no cases can be considered as fine
        if not isinstance(cases, dict):
            data = {}
            status = 200
        # if the result is True, returns 200
        elif service_result[0] in cases:
            if isinstance(cases[code], tuple):
                data = {'message': cases[code][0], 'code': code.name}
                status = cases[code][1]
            elif callable(cases[code]):
                data = cases[code](result)
                status = 200
            else:
                data = cases[code]
                status = 200
        else:
            data = {'message': "Unknown error"}
            status = 500

        return data, status
