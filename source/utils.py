from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, result=None, result_code=400):
        data = {
            'result': result,
            'resultCode': result_code
        }
        super().__init__(data=data, status=result_code)
