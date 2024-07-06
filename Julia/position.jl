using JSON

global planets

function loadData(epoch)
    global planets
    file = JSON.parsefile("data.json")
    planets = file[epoch]
end

function calcM(m0, t0, p, t)
    M = m0 + 2π * (t - t0) / p
    return M
end

function calcE(M, e)
    E = M
    for i in 1:10
        E = E - (M - E + e * sin(E)) / (e * cos(E) - 1.0)
    end
    return E
end

function calcPosition(name, t)
    t0 = planets["epoch"]
    data = planets[name]
    incl = deg2rad(data["incl"])
    lan = deg2rad(data["lan"])
    peri = deg2rad(data["lperi"] - data["lan"])
    a = data["a"]
    e = data["e"]
    m0 = deg2rad(data["m0"])
    p = data["p"]
    

    E = calcE(calcM(m0,t0,p,t), e)
    X = a * cos(E)
    Y = sqrt(1.0 - e^2) * a * sin(E)
    pos = [
        cos(lan) -sin(lan) 0.0
        sin(lan) cos(lan) 0.0
        0.0 0.0 1.0
    ] * [
        1.0 0.0
        0.0 cos(incl)
        0.0 sin(incl)
    ] * [
        cos(peri) -sin(peri)
        sin(peri) cos(peri)
    ] * [
        X-a*e
        Y
    ]
    return pos
end

loadData("2024-03-31")

t = 2460401.5
for (key, value) in planets
    if key != "epoch"
        pos = calcPosition(key, t)
        println(key, pos)
    end
end
    