class HandleReturn():
    def response(self, code, result, data):
        """response cho các api

        Args:
            code (int): response code
            result (bool): brief result
            data (str | list): result's details

        Returns:
            {
                'code': code,
                'result': result,
                'data': data
            }
        """
        return {
            'code': code,
            'result': result,
            'data': data
        }