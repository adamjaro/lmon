# Geant simulation of luminosity monitor for the EIC at BNL

## Dependencies

- Geat 4
- ROOT 5/6
- boost (already required by ROOT)

## Steps to checkout the repository and compile

<pre><code> git clone https://github.com/adamjaro/lmon.git </pre></code>
<pre><code> cd lmon </pre></code>
<pre><code> mkdir build </pre></code>
<pre><code> cd build </pre></code>
<pre><code> cmake ../ </pre></code>
<pre><code> make </pre></code>

## Run

- Run as a batch job for a given number of events

<pre><code> ./run run.mac </pre></code>

- Or run with visualization

<pre><code> ./run </pre></code>

