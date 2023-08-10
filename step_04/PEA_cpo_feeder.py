import pandapower as pp

# define network
net = pp.create_empty_network()

# create buses
bus_grid = pp.create_bus(net, vn_kv=20., name="Grid Connection")
bus_cpo_1 = pp.create_bus(net, vn_kv=20., name="Bus 1")
bus_cpo_2 = pp.create_bus(net, vn_kv=20., name="Bus 2")
bus_cpo_3 = pp.create_bus(net, vn_kv=20., name="Bus 3")
bus_cpo_4 = pp.create_bus(net, vn_kv=20., name="Bus 4")
bus_load = pp.create_bus(net, vn_kv=20., name="Bus 5")

# create ext grid
ext_grid = pp.create_ext_grid(net, bus=bus_grid, vm_pu=1.02, name="Grid Connection")

# create lines
line0 = pp.create_line(net, bus_grid, bus_cpo_1, length_km=2, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 1")
line1 = pp.create_line(net, bus_cpo_1, bus_cpo_2, length_km=2, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 1")
line2 = pp.create_line(net, bus_cpo_2, bus_cpo_3, length_km=2, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 2")
line3 = pp.create_line(net, bus_cpo_3, bus_cpo_4, length_km=2, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 3")
line4 = pp.create_line(net, bus_cpo_4, bus_load, length_km=2, std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 4")

# create loads
pp.create_load(net, bus_cpo_1, p_mw=0., q_mvar=0., name="CPO 1")
pp.create_load(net, bus_cpo_2, p_mw=0., q_mvar=0., name="CPO 2")
pp.create_load(net, bus_cpo_3, p_mw=0., q_mvar=0., name="CPO 3")
pp.create_load(net, bus_cpo_4, p_mw=0., q_mvar=0., name="CPO 4")
pp.create_load(net, bus_load, p_mw=0., q_mvar=0., name="Load")

if __name__ == '__main__':
    pp.runpp(net)
    print(net.res_bus)
    print(net.res_line)