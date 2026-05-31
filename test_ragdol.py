import sys, random
random.seed(1) # make the simulation the same each time, easier to debug
import pygame
import pymunk
import pymunk.pygame_util



def add_ragdoll(space, position=(300, 300), group=1):
    # Simple ragdoll: torso (box), head (circle), two legs (segments)
    x, y = position

    # Torso
    torso = pymunk.Body(10, 100)
    torso.position = (x, y)
    torso_shape = pymunk.Poly.create_box(torso, (14, 20))
    torso_shape.friction = 1
    torso_shape.filter = pymunk.ShapeFilter(group=group)
    torso_shape.part = 'body'

    # Head
    head = pymunk.Body(2, 10)
    head.position = (x, y - 15)
    head_shape = pymunk.Circle(head, 12)
    head_shape.friction = 1
    head_shape.filter = pymunk.ShapeFilter(group=group)
    head_shape.part = 'head'

    # Left leg
    left_leg = pymunk.Body(4, 50)
    left_leg.position = (x - 15, y + 40)
    left_leg_shape = pymunk.Segment(left_leg, (0, 0), (0, 16), 6.0)
    left_leg_shape.friction = 1
    left_leg_shape.filter = pymunk.ShapeFilter(group=group)
    left_leg_shape.part = 'leg'

    # Right leg
    right_leg = pymunk.Body(4, 50)
    right_leg.position = (x + 15, y + 40)
    right_leg_shape = pymunk.Segment(right_leg, (0, 0), (0, 16), 6.0)
    right_leg_shape.friction = 1
    right_leg_shape.filter = pymunk.ShapeFilter(group=group)
    right_leg_shape.part = 'leg'

    # Left arm
    left_arm = pymunk.Body(4, 50)
    left_arm.position = (x - 18, y - 10)
    left_arm_shape = pymunk.Segment(left_arm, (0, 0), (0, 16), 6.0)
    left_arm_shape.friction = 1
    left_arm_shape.filter = pymunk.ShapeFilter(group=group)
    left_arm_shape.part = 'arm'

    # right arm
    right_arm = pymunk.Body(4, 50)
    right_arm.position = (x + 18, y - 10)
    right_arm_shape = pymunk.Segment(right_arm, (0, 0), (0, 16), 6.0)
    right_arm_shape.friction = 1
    right_arm_shape.filter = pymunk.ShapeFilter(group=group)
    right_arm_shape.part = 'arm'


    # Joints: head to torso, legs to torso
    headjoint = pymunk.PivotJoint(head, torso, (0, 12), (0, -15))
    leg1joint = pymunk.PivotJoint(torso, left_leg, (-8, 12), (0, 0))
    leg2joint = pymunk.PivotJoint(torso, right_leg, (8, 12), (0, 0))
    arm1joint = pymunk.PivotJoint(torso, left_arm, (-8, -12), (0, 0))
    arm2joint = pymunk.PivotJoint(torso, right_arm, (8, -12), (0, 0))


    springs = [pymunk.DampedRotarySpring(head, torso, 0, 100000, 2000), pymunk.DampedRotarySpring(torso, left_leg, -0.05, 100000, 2000), pymunk.DampedRotarySpring(torso, right_leg, 0.05, 100000, 2000), pymunk.DampedRotarySpring(torso, left_arm, -0.05, 100000, 2000), pymunk.DampedRotarySpring(torso, right_arm, 0.05, 100000, 2000)]
    space.add(torso, torso_shape,
              head, head_shape,
              left_leg, left_leg_shape, left_arm, left_arm_shape,
              right_leg, right_leg_shape, right_arm, right_arm_shape, arm1joint, arm2joint,
              headjoint, springs[0], springs[1], springs[2], leg1joint, leg2joint) 
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Ragdoll")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 900)

    # add a static floor near the bottom of the window
    floor = pymunk.Segment(space.static_body, (0, 580), (600, 580), 5.0)
    floor.friction = 1
    space.add(floor)

    add_ragdoll(space, (300, 300), 1)

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
        

        screen.fill((255,255,255))
        
         


        space.debug_draw(draw_options)

        space.step(1/50)

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    main()