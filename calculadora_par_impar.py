import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

t = sp.Symbol("t", real=True)
TRANSFORMACIONES = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)
FUNCIONES = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "exp": sp.exp,
    "sqrt": sp.sqrt,
    "abs": sp.Abs,
    "ln": sp.log,
    "log": sp.log,
    "pi": sp.pi,
    "e": sp.E,
    "u": lambda x: sp.Heaviside(x, 1),
    "sign": sp.sign,
}


def descomponer(expresion: str, variable: str = "t") -> dict:
    simbolo = sp.Symbol(variable, real=True)
    contexto = {**FUNCIONES, variable: simbolo}
    x = parse_expr(
        expresion.replace("^", "**"),
        local_dict=contexto,
        transformations=TRANSFORMACIONES,
    )
    x_inv = x.subs(simbolo, -simbolo)
    par = sp.simplify((x + x_inv) / 2)
    impar = sp.simplify((x - x_inv) / 2)

    if sp.simplify(x - par) == 0:
        tipo = "par"
    elif sp.simplify(x - impar) == 0:
        tipo = "impar"
    else:
        tipo = "ni par ni impar"

    return {
        "x": str(x),
        "x_menos": str(x_inv),
        "par": str(par),
        "impar": str(impar),
        "tipo": tipo,
        "latex": {
            "x": sp.latex(x),
            "par": sp.latex(par),
            "impar": sp.latex(impar),
        },
    }


def evaluar(expresion: str, valores: list, variable: str = "t") -> dict:
    simbolo = sp.Symbol(variable, real=True)
    resultado = descomponer(expresion, variable)
    par = sp.sympify(resultado["par"], locals={variable: simbolo, **FUNCIONES})
    impar = sp.sympify(resultado["impar"], locals={variable: simbolo, **FUNCIONES})
    return {
        "t": valores,
        "par": [float(par.subs(simbolo, v)) for v in valores],
        "impar": [float(impar.subs(simbolo, v)) for v in valores],
    }


if __name__ == "__main__":
    from flask import Flask, jsonify, request
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app)

    @app.post("/api/descomponer")
    def api_descomponer():
        datos = request.get_json(silent=True) or {}
        expresion = datos.get("expresion", "").strip()
        if not expresion:
            return jsonify({"error": "Falta la expresión"}), 400
        try:
            return jsonify(descomponer(expresion))
        except Exception as error:
            return jsonify({"error": f"Expresión inválida: {error}"}), 400

    @app.post("/api/evaluar")
    def api_evaluar():
        datos = request.get_json(silent=True) or {}
        expresion = datos.get("expresion", "").strip()
        inicio = float(datos.get("inicio", -5))
        fin = float(datos.get("fin", 5))
        puntos = int(datos.get("puntos", 200))
        if not expresion or puntos < 2 or puntos > 2000:
            return jsonify({"error": "Parámetros inválidos"}), 400
        paso = (fin - inicio) / (puntos - 1)
        valores = [inicio + i * paso for i in range(puntos)]
        try:
            return jsonify(evaluar(expresion, valores))
        except Exception as error:
            return jsonify({"error": f"Expresión inválida: {error}"}), 400

    app.run(debug=True)
