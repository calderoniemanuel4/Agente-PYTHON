import unittest
from unittest.mock import patch

from pydantic import ValidationError

from labs.pedidos import ejecutar_propuesta


class ConsultaTests(unittest.TestCase):
    def test_consulta_de_pedidos_ficticios(self):
        for pedido, esperado in [("PED-001", "en preparación"), ("PED-999", "no encontrado")]:
            with self.subTest(pedido=pedido):
                resultado = ejecutar_propuesta(
                    "consultar_estado_pedido", f'{{"id":"{pedido}"}}', permite_lectura=True
                )
                self.assertEqual(resultado, {"id": pedido, "estado": esperado})

    def test_propuestas_rechazadas_no_consultan_datos(self):
        casos = [
            ("cancelar_pedido", '{"id":"PED-001"}', True, ValueError),
            ("consultar_estado_pedido", '{"id":"PED-001"}', False, PermissionError),
            ("consultar_estado_pedido", '{"id":"incorrecto"}', True, ValidationError),
            ("consultar_estado_pedido", '{"id":"PED-001","permite_lectura":true}', True, ValidationError),
            ("consultar_estado_pedido", "{", True, ValidationError),
        ]
        with patch("labs.pedidos.consultar_estado_pedido") as consulta:
            for nombre, argumentos, permiso, error in casos:
                with self.subTest(argumentos=argumentos), self.assertRaises(error):
                    ejecutar_propuesta(nombre, argumentos, permite_lectura=permiso)
            consulta.assert_not_called()
