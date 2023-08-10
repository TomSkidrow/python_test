import pandapower as pp

# Define network
net = pp.create_empty_network()

# Create buses
b1 = pp.create_bus(net, vn_kv=20.)
b2 = pp.create_bus(net, vn_kv=20.)
b3 = pp.create_bus(net, vn_kv=20.)
b4 = pp.create_bus(net, vn_kv=20.)
b5 = pp.create_bus(net, vn_kv=20.)
b6 = pp.create_bus(net, vn_kv=20.)

# Create external grid (slack bus) at bus 0
pp.create_ext_grid(net, bus=b1, vm_pu=1.02)

# Create load at bus 2
pp.create_load(net, bus=b2, p_mw=1.)

# Create line element
pp.create_line(net, from_bus=b1, to_bus=b2, length_km=2.0,
               std_type="NA2XS2Y 1x240 RM/25 12/20 kV")
