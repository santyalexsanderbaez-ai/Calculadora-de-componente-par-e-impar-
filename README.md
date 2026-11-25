# Calculadora de componentes par e impar

Calcula la descomposición de una señal x(t) en sus componentes par e impar:

- Componente par: x_e(t) = [x(t) + x(−t)] / 2
- Componente impar: x_o(t) = [x(t) − x(−t)] / 2

Además indica si la señal original es par, impar o ninguna de las dos. Incluye una API con Flask para conectarla a una página web.

## Requisitos

- Python 3.9 o superior

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python calculadora_par_impar.py
```

El servidor queda disponible en `http://127.0.0.1:5000`.

### Endpoint `/api/descomponer`

Método `POST`. Cuerpo:

```json
{ "expresion": "t^2 + sin(t) + exp(t)" }
```

Respuesta:

```json
{
  "x": "...",
  "x_menos": "...",
  "par": "...",
  "impar": "...",
  "tipo": "ni par ni impar",
  "latex": { "x": "...", "par": "...", "impar": "..." }
}
```

### Endpoint `/api/evaluar`

Método `POST`. Devuelve puntos numéricos de ambas componentes para graficarlas.

```json
{ "expresion": "t^2 + sin(t)", "inicio": -5, "fin": 5, "puntos": 200 }
```

## Funciones admitidas

`sin`, `cos`, `tan`, `exp`, `sqrt`, `abs`, `ln`, `log`, `sign`, `pi`, `e` y el escalón `u(t)`. Las potencias se escriben con `^`.

## Ejemplo desde JavaScript

```javascript
const respuesta = await fetch("http://127.0.0.1:5000/api/descomponer", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ expresion: "t^2 + sin(t) + exp(t)" })
});
const datos = await respuesta.json();
```
