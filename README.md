# Timing-Dispersion-Strategy-requires-Deutsche-Boerse-A7-access
--A simple way to know when to enter dispersion strategy--

A Dispersion Strategy is a way for option traders to take advantage of the premium in index implicit volatility compared to single stock's volatility.
This premium comes from different flows in each asset class :
- Global hedge on index options
- Overwriting strategies on single stocks options

See a more detailed explanation at :
https://blog.quantinsti.com/dispersion-trading-using-options/#:~:text=The%20Dispersion%20Trading%20is%20a,than%20between%20individual%20stock%20options.

A dispersion strategy is sometimes said to be equivalent to trading the intra index correlation but it is a misleading approach.
The purest form of dispersion is via Varswap on index vs Varswap on underlyings.
This is not how it is traded nowadays though, as varswaps are deemed too dangerous in market dislocation scenarios, but options based dispersion portfollio can locally replicate varswap trades. For this reason, the varswap approach can still be a good way to evaluate a dispersion strategy.

The Dispersion Volatility measure is :

Dispersion_Vol = ( Sum(i=1..n, W_i * ATF_i^2) - (1+Leverage) * ATF_index^2 ) / Normalisation_factor

where

- ATF_i is the ATM Forward implicit vol of the ith stock in the index
- ATF_index is the ATM Forward implicit vol of the index
- Leverage is the additional notional of index varswap to sell in order to get a vega neutral dispersion. Typically 20%.
- W_i is the weight of the ith component in the index
- Normalisation_factor is a factor to apply to get a vega of 1 on the index so : 2 * (1+Leverage) * ATF_index


Explanation :
It is a measure of the price of a varswap dispersion strategy with a leverage on the index in order to target a vega neutral portfolio.

This indicator can of course also be computed in a realized form instead of implicit, simply by inputing realized volatilities instead. 
The PnL of the dispersion strategy will then be very straight forward :
PnL = Dispersion_Vol_Realized - Dispersion_Vol_Implicit

Consequently, the lower the implicit Dispersion_Vol, the higher the chances of positive reward.


What we will be doing :
Option traders know that when markets collapse, the index vol overshoots the vol of components which generates dispersion trade opportunities.
Visually, this creates a clockwise patterns on a graph representing the Dispersion_Vol on the Y axis and the index implicit vol on the X axis in case of market stress :
- First index vol rises and overshoots stock vol so the dispersion vol goes down -> the curve moves to right and lower.
- Then the stock vol rises pushing the disp vol higher so the curve moves up.
- Finally, the market settles and reverts to its original level completing the anti clockwise trajectory.

The goal of this git is show how to create this graph using Deutsche Boerse's A7 API.

Here are some examples :


March 2020 market meltdown :

![plot](./Graphs/myplot_March_2020.png)


January 2020 :

![plot](./Graphs/myplot_Jan_2020.png)


Nov 2019 to Oct 2020 :

![plot](./Graphs/myplot_Nov_2019_to_Oct_2020.png)
