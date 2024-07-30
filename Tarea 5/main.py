import  streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main():
    def calculate_pi(n):
        x = np.random.rand(1, n)
        y = np.random.rand(1, n)
        r = np.sqrt(np.square(x) + np.square(y))
        mask = r <= 1
        aprox_pi = np.sum(mask) / n * 4
        return aprox_pi, x, y, mask

    st.title('Aproximación de π usando el Método de Monte Carlo')


    st.write("""
### Explicación del Método
La idea básica es que:

$$
\\frac{\\pi r^2}{4 r^2} \\approx \\frac{\\text{número de puntos dentro del círculo}}{\\text{número de puntos dentro del cuadrado}}
$$

Por lo tanto,

$$
\\pi \\approx 4 \\frac{\\text{número de puntos dentro del círculo}}{\\text{número de puntos dentro del cuadrado}}
$$
""")

    # Entradas del usuario
    num_simulations = st.slider('Número de Simulaciones', 10, 100000, 100)

    # Cálculo de π
    aprox_pi, x, y, mask = calculate_pi(num_simulations)

    # Mostrar resultado
    st.subheader(f'Aproximación de π: {aprox_pi}')

    # Gráfica del proceso
    fig, ax = plt.subplots()
    ax.plot(x[mask], y[mask], 'o', color='blue', markersize=0.5, label='Dentro del círculo')
    ax.plot(x[~mask], y[~mask], 'o', color='red', markersize=0.5, label='Fuera del círculo')
    ax.set_aspect('equal')
    ax.set_title('Simulación de Monte Carlo')
    ax.legend()
    st.pyplot(fig)

if __name__ == "__main__":
    main()
    
