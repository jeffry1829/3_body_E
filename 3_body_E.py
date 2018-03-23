from visual import *
from visual.graph import *

spring_L=0.05
ball_mass=1000
vec_g=vector(0,-1, 0)*9.8
vec_elec_field=vector(5000,0,0)
K_spring=1000000000
global_t=0
dt=0.001

scene = display(width=800, height=800, center=(0, 0, 0), userzoom=True, autoscale=True) # alt&drag to zoom | ctrl&drag to move around 
ceil = box(length=0.8, height=0.005, width=0.8, color=color.yellow, pos=(0,0,0))

gd_horizontal = gdisplay(x=800, y=0, width=400, height=400, xtitle='t', ytitle='horizontal',\
			  foreground=color.black, background=color.white,\
			  xmax=10, xmin=0, ymax=0.1, ymin=-0.1)
f_ball0_horizontal=gcurve(color=color.blue)
f_ball1_horizontal=gcurve(color=color.green)
f_ball2_horizontal=gcurve(color=color.yellow)

gd_vertical = gdisplay(x=800, y=600, width=400, height=400, xtitle='t', ytitle='vertical',\
			  foreground=color.black, background=color.white,\
			  xmax=10, xmin=0, ymax=-0.01, ymin=-0.2) 
f_ball0_vertical=gcurve(color=color.blue)
f_ball1_vertical=gcurve(color=color.green)
f_ball2_vertical=gcurve(color=color.yellow)

balls = [sphere(radius = 0.01, color=color.red, pos=(0,-0.05,0), Q=-2, mass=ball_mass, connect_spring=[0,1]), \
		 sphere(radius = 0.01, color=color.red, pos=(0,-0.10,0), Q=+3, mass=ball_mass, connect_spring=[1,2]), \
		 sphere(radius = 0.01, color=color.red, pos=(0,-0.15,0), Q=-1, mass=ball_mass, connect_spring=[2]  )]
for index, ball in enumerate(balls):
	ball.v=vector(0,0,0)
	ball.a=vector(0,0,0)

springs = [helix(radius=0.0001, thickness=0.001, color=color.red) for i in range(3)]

arrows= [arrow(shaftwidth=0.01) for i in range(3)]

def HookForce(vec_springTomass, length_spring, k):
    return -k*(vec_springTomass.mag - length_spring) * (vec_springTomass/vec_springTomass.mag)

#MassCenter for simple system
def MassCenter(list_balls):
	sigma_pos=vector(0,0,0)
	for ball in list_balls:
		sigma_pos += ball.pos
	return sigma_pos/len(list_balls)

while True:
	#set up arrows
	for index, arrow in enumerate(arrows):
		arrow.pos = balls[index].pos
		#arrow showing acceleration of electric field
		arrow.axis= vec_elec_field * balls[index].Q * (0.00001) #avoid exceed length of arrow
	
	#detect if anytime ball[0],ball[2]'s x=0 and ball[1]'s x>0
	#vacant
	#graphing mass center
	sphere(radius=0.005, color=color.blue, pos=MassCenter(balls))

	#plot graph
	f_ball0_horizontal.plot(pos=vector(global_t, balls[0].pos.x))
	f_ball1_horizontal.plot(pos=vector(global_t, balls[1].pos.x))
	f_ball2_horizontal.plot(pos=vector(global_t, balls[2].pos.x))
	
	f_ball0_vertical.plot(pos=vector(global_t, balls[0].pos.y))
	f_ball1_vertical.plot(pos=vector(global_t, balls[1].pos.y))
	f_ball2_vertical.plot(pos=vector(global_t, balls[2].pos.y))
	
	#rate
	rate(1000)
	
	#set springs' pos and axis
	for index, spring in enumerate(springs):
		if index==0:
			spring.pos=ceil.pos
			spring.axis=balls[index].pos-ceil.pos
		else:
			spring.pos=balls[index-1].pos
			spring.axis=balls[index].pos-balls[index-1].pos

	#set balls' motion
	for index, ball in enumerate(balls):
		ball.a=vector(0,0,0)
		if index==2:
			ball.a += (ball_mass*vec_g + vec_elec_field*ball.Q + HookForce(springs[index].axis, spring_L, K_spring))/ball_mass
		else:
			ball.a += (ball_mass*vec_g + vec_elec_field*ball.Q +\
			HookForce(springs[index].axis, spring_L, K_spring)+\
			-HookForce(springs[index+1].axis, spring_L, K_spring))/ball_mass
		ball.v += ball.a*dt
		ball.pos += ball.v*dt
	
	#timer
	global_t+=dt
	