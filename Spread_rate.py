import numpy as np
from scipy.integrate import odeint
import streamlit as st
import matplotlib.pyplot as plt

# Function to define the SEIR model differential equations
def deriv(y, t, N, beta, sigma, gamma):
    S, E, I, R = y
    dSdt = -beta * S * I / N
    dEdt = beta * S * I / N - sigma * E
    dIdt = sigma * E - gamma * I
    dRdt = gamma * I
    return dSdt, dEdt, dIdt, dRdt

# Function to run the SEIR model simulation
def run_seir_model(N, initial_infected, beta, sigma, gamma, days):
    # Initial number of exposed, infected, and recovered individuals, everyone else is susceptible to infection initially.
    E0, I0, R0 = 0, initial_infected, 0
    S0 = N - E0 - I0 - R0

    # A grid of time points (in days)
    t = np.linspace(0, days, days)

    # Initial conditions vector
    y0 = S0, E0, I0, R0

    # Integrate the SEIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, sigma, gamma))
    S, E, I, R = ret.T

    # Plot the data on three separate curves for S(t), E(t), I(t), and R(t)
    st.pyplot(plt.figure(figsize=(10, 6)))
    plt.plot(t, S, 'b', label='Susceptible')
    plt.plot(t, E, 'y', label='Exposed')
    plt.plot(t, I, 'r', label='Infected')
    plt.plot(t, R, 'g', label='Recovered')
    plt.xlabel('Days')
    plt.ylabel('Population')
    plt.title('SEIR Model Simulation')
    plt.legend()
    st.pyplot(plt)

scale_popu_dense = """ Very Low (1-2): Sparse crowd, with significant gaps between individuals. Plenty of personal space.\n\n
Low (3-4): A small gathering with more people present, but still with ample personal space.\n\n
Moderate (5-6): An average-sized crowd where individuals are closer together, but there is still some personal space.\n\n
High (7-8): A dense crowd where personal space is limited, and individuals are in close proximity.\n\n
Very High (9-10): Extremely dense crowd, minimal personal space, and potential for discomfort or safety concerns due to overcrowding."""

# Streamlit app
st.title('SEIR Model Simulation')

# User inputs
population_size = st.number_input("Enter the total population size:", min_value=1.0, step=1.0)
initial_infected = st.number_input("Enter the initial number of infected individuals:", min_value=0.0, step=1.0)
if initial_infected<population_size:
  beta = st.number_input("Enter the contact rate:", min_value=0.0)
  st.warning(scale_popu_dense)
  sigma = st.number_input("Enter the time period for a person to be able to infect others:", min_value=0.0)
  gamma = st.number_input("Enter the recovery rate/time to recover (in days):", min_value=0.0)
  simulation_days = st.number_input("Enter the duration(in days) for you want to check spread:", min_value=1, step=1)
  run_seir_model(population_size, initial_infected, beta, sigma, gamma, simulation_days)
else:
  st.write("initial infected people should be less than or equal of total population")
