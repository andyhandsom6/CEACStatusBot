import unittest
from unittest.mock import MagicMock, patch

from CEACStatusBot.request.query import query_status


class CloudflareBlockTest(unittest.TestCase):
    @patch("CEACStatusBot.request.query.requests.Session")
    def test_403_stops_without_retry_or_attempting_captcha(self, session_class):
        response = MagicMock()
        response.status_code = 403
        response.headers = {"Server": "cloudflare", "Content-Type": "text/html"}
        response.text = "<html><title>Attention Required! | Cloudflare</title></html>"
        response.url = "https://ceac.state.gov/CEACStatTracker/Status.aspx?App=NIV"
        session_class.return_value.get.return_value = response
        captcha_solver = MagicMock()

        with self.assertRaisesRegex(RuntimeError, "Cloudflare.*HTTP 403"):
            query_status(
                "CHINA, SHENYANG", "AA00000000", "EXAMPLE000",
                "EXAMP", captchaHandle=captcha_solver
            )

        session_class.return_value.get.assert_called_once()
        captcha_solver.solve.assert_not_called()


if __name__ == "__main__":
    unittest.main()
