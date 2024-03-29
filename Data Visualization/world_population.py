import json

import pygal
from pygal.maps.world import World
from pygal.maps.world import COUNTRIES

from pygal.style import RotateStyle as RS, LightColorizedStyle as LCS


from country_codes import get_country_code

filename = 'C:\\spyder_mj\\project_01\\Chapter_01\\data_visualization\\population_data.json'

print (filename)
with open(filename) as f:
    pop_data = json.load(f)

    cc_populations = {}
    for pop_dict in pop_data:
        if pop_dict['Year'] == '2010':
            country_name = pop_dict['Country Name']
            population = int(float(pop_dict['Value']))
            #print(population)
            code = get_country_code(country_name)
            if code:
                cc_populations[code] = population
            else:
                #print('error ', country_name)
                pass

    cc_pops_1, cc_pops_2, cc_pops_3 = {},{},{}
    for cc, pop in cc_populations.items():
        if pop < 10000000:
            cc_pops_1[cc] = pop
        elif pop < 1000000000:
            cc_pops_2[cc] = pop
        else:
            cc_pops_3[cc] = pop

    print(len(cc_pops_1),len(cc_pops_2),len(cc_pops_3))

    #wm_style = RS('#336699', base_style = LCS) 
    wm_style = LCS
    wm = pygal.maps.world.World(style=wm_style)
    wm.title = 'World Population in 2010 by Country'
    wm.add('0-10m',cc_pops_1)
    wm.add('10m-1bn',cc_pops_2)
    wm.add('>1bn',cc_pops_3)

    
    #wm.pygal.Worldmap(style=wm_style)
    wm.render_to_file('C:/Users/mlingaiah/source/repos/Alien_Invasion/Weather/world_population.svg')