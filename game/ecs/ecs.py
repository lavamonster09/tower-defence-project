from game.ecs.entity import *
from game.ecs.components import *

class Ecs:
	def __init__(self):
		self.entities = []

	def add_entity(self, *components):
		entity = Entity()
		self.entities.append(entity)
		for component in component:
			self.add_component(component, entity)
		return entity

	def add_component(self, component: Component, target: Entity):
		target.add_component(component)