import pygal
from pygal.maps.world import World

wm = pygal.maps.world.World()
wm.title = 'Populations of Countries in NA'
wm.add('North America', {'ca' : 34126000, 'us' : 309349000, 'mx' : 113423000})
wm.render_to_file('C:/Users/mlingaiah/source/repos/Alien_Invasion/Weather/na_population.svg')