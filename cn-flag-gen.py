#!/usr/bin/env python3

from math import atan2,degrees,sin,cos,pi,sqrt,fabs
from collections import namedtuple
import jinja2 
import sys

StarPosition = namedtuple('StarPosition','cx cy angle')

cn_flag_template = jinja2.Template(
'''
<?xml version="1.0" standalone="no"?>
<svg id="cn-flag" width="600" height="400" viewBox="0 0 30 20" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <symbol id="star5" viewBox="-1 -1 2 2">
    <polygon points="{{ star_points }}" fill="yellow"/>
  </symbol>
  <rect width="30" height="20" fill="red"/>
  <use xlink:href="#star5" x="{{ mp.cx-3 }}"  y="{{ mp.cy-3 }}" width="6" height="6"/>
{%- for p in sstar_positions %}
  <use xlink:href="#star5" x="{{ p.cx-1 }}"  y="{{ p.cy-1 }}" width="2" height="2" transform="rotate({{ "%f,%d,%d"%(p.angle,p.cx,p.cy) }})"/>
{%- endfor %}
{% if show_aux %}
  <!-- auxiliary lines -->
{%- set aux_style = 'stroke="gray" stroke-width="0.01"' %}
{% for i in range(1,10) %}
  <line x1="0" y1="{{ i }}" x2="15" y2="{{ i }}" {{ aux_style }} />
{%- endfor %}
{% for i in range(1,15) %}
  <line x1="{{ i }}" y1="0" x2="{{ i }}" y2="10" {{ aux_style }} />
{%- endfor %}
  <circle cx="5" cy="5" r="3" {{ aux_style }} fill="none" />
{% for p in sstar_positions %}
  <line x1="5" y1="5" x2="{{ p.cx }}" y2="{{ p.cy }}" {{ aux_style }} />
  <circle cx="{{ p.cx }}" cy="{{ p.cy }}" r="1" {{ aux_style }} fill="none" />
{%- endfor %}
  <line x1="0" y1="10" x2="30" y2="10" {{ aux_style }} stroke-dasharray="1 0.2 0.2 0.2"/>
  <line x1="15" y1="0" x2="15" y2="20" {{ aux_style }} stroke-dasharray="1 0.2 0.2 0.2"/>
{% endif -%}
</svg> 
'''.lstrip())

# points on a star
star_points = ''
for i in range(0,10):
    angle = -pi/2+2*pi/10*i
    r = 1 if i%2==0 else (3-sqrt(5))/2
    x = round(r*cos(angle), 10)
    y = round(r*sin(angle), 10)
    star_points += str(x)+' '
    star_points += str(y)+' '

# main star's position
mp = StarPosition(cx=5, cy=5, angle=0)

# the four smaller stars
sstar_positions = []
for xy in [(10,2),(12,4),(12,7),(10,9)]:
    cx, cy = xy
    angle = -degrees(atan2(cx-5, cy-5)) 
    sstar_positions.append(StarPosition(cx, cy, angle))

show_aux = False
if len(sys.argv)>=2 and sys.argv[1]=='--show-aux' :
    show_aux = True

print(cn_flag_template.render(locals()))
