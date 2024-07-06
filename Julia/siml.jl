using Statistics

function getAcc(pos, mass, G, softening)
    x = pos[:, 1:1]
    y = pos[:, 2:2]
    z = pos[:, 3:3]

    dx = x' - x
    dy = y' - y
    dz = z' - z

    inv_r3 = (dx^2 + dy^2 + dz^2 + softening^2)^(-1.5)

    ax = G * (dx * inv_r3) * mass
    ay = G * (dy * inv_r3) * mass
    az = G * (dz * inv_r3) * mass

    a = hcat(ax,ay,az)

    return a
end

function getEnergy(pos, vel, mass, G)
    KE = 0.5 * sum(sum(mass * vel^2))

    x = pos[:, 1:1]
    y = pos[:, 2:2]
    z = pos[:, 3:3]

    dx = x' - x
    dy = y' - y
    dz = z' - z

    inv_r = sqrt(dx^2 + dy^2 + dz^2)

    PE = G * sum(sum(triu(-(mess*mess')*inv_r,1)))

    return KE, PE
end

function main()
    N = 2
    t = 0
    tEnd = 2.0
    dt = 0.01
    softening = 0.1
    G = 1.0
    plotRealTime = true
    
    mass = [20 1]
    pos = [
        0 0 0
        10 0 0
    ]
    vel = [
        0 0 0
        0 1 0
    ]
    vel -= mean(mass * vel, 0) / mean(mass)
    acc = getAcc(pos, mass, G, softening)
    KE, PE = getEnergy(pos, vel, mass, G)
    Nt = Int(ceil(tEnd/dt))

    pos_save = zeros((N,3,Nt+1))
    pos_save[:,:,1] = pos
    KE_save = zeros(Nt)
    KE_save[1] = KE
    PE_save = zeros(Nt)
    PE_save[1] = PE
    t_all = range(Nt)*dt

    for i in 1:Nt
        vel += acc * dt/2.0
        pos += vel * dt
        acc = getAcc(pos, mass, G, softening)
        vel += acc * dt/2.0
        t += dt

        KE, PE = getEnergy(pos, vel, mass, G)
        pos_save[:,:,i+1] = pos
        KE_save[i+1] = KE
        PE_save[i+1] = PE

        if plotRealTime || i == Nt - 1
            println(pos)
        end

    end
end

main()