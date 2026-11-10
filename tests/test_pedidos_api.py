import json
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from labs.pedidos_api import preguntar


class PedidosAPITests(unittest.TestCase):
    def test_devuelve_estado_local_con_el_id_de_la_llamada(self):
        client = Mock()
        llamada = SimpleNamespace(type="function_call", name="consultar_estado_pedido",
                                  arguments='{"id":"PED-002"}', call_id="consulta-1")
        client.responses.create.side_effect = [
            SimpleNamespace(id="turno-1", output=[llamada]),
            SimpleNamespace(output_text="El pedido fue enviado."),
        ]
        self.assertEqual(preguntar(client, "¿Y el PED-002?", modelo="test", permite_lectura=True),
                         "El pedido fue enviado.")
        segunda = client.responses.create.call_args.kwargs
        self.assertEqual(segunda["previous_response_id"], "turno-1")
        salida, = segunda["input"]
        self.assertEqual(salida["call_id"], "consulta-1")
        self.assertEqual(json.loads(salida["output"]), {"id": "PED-002", "estado": "enviado"})

    def test_aclaracion_no_ejecuta_herramientas(self):
        client = Mock()
        client.responses.create.return_value = SimpleNamespace(output=[], output_text="¿Qué ID?")
        with patch("labs.pedidos_api.ejecutar_propuesta") as ejecutar:
            self.assertEqual(preguntar(client, "¿Ya salió?", modelo="test", permite_lectura=True),
                             "¿Qué ID?")
            ejecutar.assert_not_called()
        client.responses.create.assert_called_once()

    def test_sin_permiso_no_contacta_al_modelo(self):
        client = Mock()
        with self.assertRaises(PermissionError):
            preguntar(client, "Consultá PED-001", modelo="test", permite_lectura=False)
        client.responses.create.assert_not_called()
