from xmlrpc.client import FastParser
import pygame
from constants import *
from player import *
from units import *

pygame.init()
pygame.display.init()
pygame.font.init()

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castles War')


# variables
turns = 0
blue_turn = True
blue_info = [blue_player.wall]
red_info = [red_player.wall]
worker_list = []
swordsman_list = []
archer_list = []
pause = False
bluetower_rest = 0
redtower_rest = 0
blue_workers = 0
red_workers = 0
turn_time = 0

# fonts
font = pygame.font.Font('fonts/font.ttf', 16)
big_font = pygame.font.Font('fonts/font.ttf', 24)


if __name__ == "__main__":

    run = True
    keys = []

    
    def display(win):
        # displaying the ground
        win.fill((0, 255, 0), (0, SCREEN_HEIGHT-GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        win.blit(backgorund_img, (0, 0))
        
        # displaying the towers
        win.blit(btower_img, (WALL_POS - btower_img.get_width()/2, SCREEN_HEIGHT - GROUND_HEIGHT - TOWER_HEIGHT + 10))
        win.blit(rtower_img, (SCREEN_WIDTH - WALL_POS - rtower_img.get_width()/2, SCREEN_HEIGHT - GROUND_HEIGHT - TOWER_HEIGHT + 10))

        # displaying the barracks
        win.blit(bbarracks_img, (BARRACKS_POS - bbarracks_img.get_width()/2, SCREEN_HEIGHT - GROUND_HEIGHT - BARRACKS_HEIGHT + 10))
        win.blit(rbarracks_img, (SCREEN_WIDTH - BARRACKS_POS - rbarracks_img.get_width()/2, SCREEN_HEIGHT - GROUND_HEIGHT - BARRACKS_HEIGHT + 10))

        # displaying the mines
        win.blit(bmine_img, (MINE_POS - bmine_img.get_width()/2, SCREEN_HEIGHT - GROUND_HEIGHT - MINE_HEIGHT + 7))
        win.blit(rmine_img, (SCREEN_WIDTH - MINE_POS - rmine_img.get_width()/2, SCREEN_HEIGHT - GROUND_HEIGHT - MINE_HEIGHT + 7))

        win.blit(blue_wall_img, (WALL_POS - blue_wall_img.get_width()/2, SCREEN_HEIGHT - GROUND_HEIGHT - WALL_HEIGHT + 10))
        win.blit(red_wall_img, (SCREEN_WIDTH - WALL_POS - red_wall_img.get_width()/2, SCREEN_HEIGHT - GROUND_HEIGHT - WALL_HEIGHT + 10))
    
        # displaying the diamonds
        win.blit(res_ui_blue_img, (10, 10))
        res_text = font.render(str(blue_player.resources), 1, 'white')
        win.blit(res_text, (10 + res_ui_blue_img.get_width() - dmd_img.get_width() - 10 - font.size(str(blue_player.resources))[0], 15))

        win.blit(res_ui_red_img, (SCREEN_WIDTH - res_ui_red_img.get_width() - 10, 10))
        res_text = font.render(str(red_player.resources), 1, 'white')
        win.blit(res_text, (SCREEN_WIDTH - dmd_img.get_width() - 20 - font.size(str(red_player.resources))[0], 15))

        win.blit(dmd_img, (10 + res_ui_blue_img.get_width() - dmd_img.get_width() - 5, 18))
        win.blit(dmd_img, (SCREEN_WIDTH - dmd_img.get_width() - 15, 18))

        win.blit(res_ui_blue_img, (10, 60))
        res_text = font.render(str(blue_workers), 1, 'white')
        win.blit(res_text, (10 + res_ui_blue_img.get_width() - dmd_img.get_width() - 10 - font.size(str(blue_workers))[0], 65))

        win.blit(res_ui_red_img, (SCREEN_WIDTH - res_ui_red_img.get_width() - 10, 60))
        res_text = font.render(str(red_workers), 1, 'white')
        win.blit(res_text, (SCREEN_WIDTH - dmd_img.get_width() - 20 - font.size(str(red_workers))[0], 65))

        worker_img = pygame.image.load('images/worker.png')

        win.blit(pygame.transform.flip((worker_img), 1, 0), (10 + res_ui_blue_img.get_width() - worker_img.get_width() - 5, 68))
        win.blit(pygame.transform.flip((worker_img), 1, 0), (SCREEN_WIDTH - worker_img.get_width() - 15, 68))

        for i in range(len(workers_disp)):
            if i < len(workers_disp):
                if workers_disp[i].health <= 0:
                    workers_disp.pop(i)
                else:
                    workers_disp[i].display(win)

        for i in range(len(swords_disp)):
            if i < len(swords_disp):
                if swords_disp[i].health <= 0:
                    swords_disp.pop(i)
                else:
                    swords_disp[i].display(win)

        for i in range(len(archers_disp)):
            if i < len(archers_disp):
                if archers_disp[i].health <= 0:
                    archers_disp.pop(i)
                else:
                    archers_disp[i].display(win)

    def update():
        global blue_turn, bluetower_rest, redtower_rest, turns, blue_workers, red_workers
        global turn_time

        turns += 1

        blue_workers = blue_player.units[0]
        red_workers = red_player.units[0]

        blue_player.resources += 50
        red_player.resources += 50

        for worker in workers_disp:
            if worker.team == 'blue':
                blue_workers += 1
            else:
                red_workers += 1

        for i in range(len(worker_list)):
            if i < len(worker_list):
                if blue_turn:
                    if worker_list[i][0] == 'blue':
                        worker_list[i][1] -= 1
                else:
                    if worker_list[i][0] == 'red':
                        worker_list[i][1] -= 1
                if worker_list[i][1] <= 0:
                    if worker_list[i][0] == 'blue':
                        blue_player.units[0] += 1
                    elif worker_list[i][0] == 'red':
                        red_player.units[0] += 1
                    worker_list.pop(i)

        for i in range(len(swordsman_list)):
            if i < len(swordsman_list):
                if blue_turn:
                    if swordsman_list[i][0] == 'blue':
                        swordsman_list[i][1] -= 1
                else:
                    if swordsman_list[i][0] == 'red':
                        swordsman_list[i][1] -= 1
                if swordsman_list[i][1] <= 0:
                    if swordsman_list[i][0] == 'blue':
                        blue_player.units[1] += 1
                    elif swordsman_list[i][0] == 'red':
                        red_player.units[1] += 1
                    swordsman_list.pop(i)

        for i in range(len(archer_list)):
            if i < len(archer_list):
                if blue_turn:
                    if archer_list[i][0] == 'blue':
                        archer_list[i][1] -= 1
                else:
                    if archer_list[i][0] == 'red':
                        archer_list[i][1] -= 1
                if archer_list[i][1] <= 0:
                    if archer_list[i][0] == 'blue':
                        blue_player.units[2] += 1
                    elif archer_list[i][0] == 'red':
                        red_player.units[2] += 1
                    archer_list.pop(i)

        for worker_unit in workers_disp:
            if blue_turn:
                if worker_unit.team == 'blue' and worker_unit.status == 'mining':
                    blue_player.resources += WORKER_PROD
                elif worker_unit.team == 'blue' and worker_unit.status == 'wall' and blue_player.wall < WALL_HEALTH:
                    blue_player.wall += WORKER_REPAIR
            else:
                if worker_unit.team == 'red' and worker_unit.status == 'mining':
                    red_player.resources += WORKER_PROD
                elif worker_unit.team == 'red' and worker_unit.status == 'wall' and blue_player.wall < WALL_HEALTH:
                    red_player.wall += WORKER_REPAIR
                

        # for sword in swords_disp:
        #     if blue_turn:
        #         if sword.team == 'blue':
        #             sword.update()
        #     else:
        #         if sword.team == 'red':
        #             sword.update()

        # for archer in archers_disp:
        #     if blue_turn:
        #         if archer.team == 'blue':
        #             archer.update()
        #         elif archer.team == 'red':
        #             archer.update()

        if blue_turn:
            if bluetower_rest > 0:
                bluetower_rest -= 1
        else:
            if redtower_rest > 0:
                redtower_rest -= 1


        blue_turn = not blue_turn
        turn_time = pygame.time.get_ticks()
        
    def commands():
        if not pause:
            if blue_turn:
                if keys[pygame.K_x]:
                    update()
                if keys[pygame.K_q]:
                    if blue_player.resources >= WORKER_COST:
                        blue_player.resources -= WORKER_COST
                        worker_list.append(['blue', WORKER_TRAIN])
                        update()
                elif keys[pygame.K_w]:
                    if blue_player.resources >= SWORD_COST:
                        blue_player.resources -= SWORD_COST
                        swordsman_list.append(['blue', SWORD_TRAIN])
                        update()
                elif keys[pygame.K_e]:
                    if blue_player.resources >= ARCHER_COST:
                        blue_player.resources -= ARCHER_COST
                        archer_list.append(['blue', ARCHER_TRAIN])
                        update()
                elif keys[pygame.K_a]:
                    # worker to mine
                    if blue_player.units[0] > 0:
                        workers_disp.append(Worker('heading mining', 'blue'))
                        blue_player.units[0] -= 1
                        update()
                elif keys[pygame.K_s]:
                    # worker to wall
                    if blue_player.units[0] > 0:
                        for i in range(blue_player.units[0]):
                            workers_disp.append(Worker('heading wall', 'blue'))
                            blue_player.units[0] -= 1
                        update()
                elif keys[pygame.K_d]:
                    # swordsman attack
                    if blue_player.units[1] > 0:
                        for i in range(blue_player.units[1]):
                            swords_disp.append(Swordsman('blue'))
                            blue_player.units[1] -= 1
                        update()
                elif keys[pygame.K_f]:
                    # archer attack
                    if blue_player.units[2] > 0:
                        for i in range(blue_player.units[2]):
                            archers_disp.append(Archer('blue'))
                            blue_player.units[2] -= 1
                        update()
                elif keys[pygame.K_z]:
                    # unleash all
                    if blue_player.units[1] > 0 or blue_player.units[2] > 0:
                        x = WALL_POS
                        for archer_unit in range(blue_player.units[2]):
                            archers_disp.append(Archer('blue', x))
                            x += archers_disp[archer_unit].img.get_width() + 2
                            blue_player.units[2] -= 1

                        for sword_unit in range(blue_player.units[1]):
                            swords_disp.append(Swordsman('blue', x))
                            x += swords_disp[sword_unit].img.get_width() + 2
                            blue_player.units[1] -= 1

                        update()
            else:
                if keys[pygame.K_n]:
                    update()
                if keys[pygame.K_p]:
                    if red_player.resources >= WORKER_COST:
                        red_player.resources -= WORKER_COST
                        worker_list.append(['red', WORKER_TRAIN])
                        update()
                elif keys[pygame.K_o]:
                    if red_player.resources >= SWORD_COST:
                        red_player.resources -= SWORD_COST
                        swordsman_list.append(['red', SWORD_TRAIN])
                        update()
                elif keys[pygame.K_i]:
                    if red_player.resources >= ARCHER_COST:
                        red_player.resources -= ARCHER_COST
                        archer_list.append(['red', ARCHER_TRAIN])
                        update()
                elif keys[pygame.K_l]:
                    # worker to mine
                    if red_player.units[0] > 0:
                        workers_disp.append(Worker('heading mining', 'red'))
                        red_player.units[0] -= 1
                        update()
                elif keys[pygame.K_k]:
                    # worker to wall
                    if red_player.units[0] > 0:
                        for i in range(red_player.units[0]):
                            workers_disp.append(Worker('heading wall', 'red'))
                            red_player.units[0] -= 1
                        update()
                elif keys[pygame.K_j]:
                    # swordsman attack
                    if red_player.units[1] > 0:
                        for i in range(red_player.units[1]):
                            swords_disp.append(Swordsman('red'))
                            red_player.units[1] -= 1
                        update()
                elif keys[pygame.K_h]:
                    # archer attack
                    if red_player.units[2] > 0:
                        for i in range(red_player.units[2]):
                            archers_disp.append(Archer('red'))
                            red_player.units[2] -= 1
                        update()
                elif keys[pygame.K_m]:
                    # unleash all
                    if red_player.units[1] > 0 or red_player.units[2] > 0:
                        x = SCREEN_WIDTH - WALL_POS - 20
                        for archer_unit in range(red_player.units[2]):
                            archers_disp.append(Archer('red', x))
                            x += archers_disp[archer_unit].img.get_width() - 22
                            red_player.units[2] -= 1

                        for sword_unit in range(red_player.units[1]):
                            swords_disp.append(Swordsman('red', x))
                            x += swords_disp[sword_unit].img.get_width() - 22
                            red_player.units[1] -= 1

                        update()


    while run:

        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                with open('game_data.txt', 'w') as f:
                    f.write('START Game\n')
                    f.write(f'TURN {turns}\n')
                    f.write('END Game\n\n')
                    f.write('START Player1\n')
                    f.write(f'WALL {blue_player.wall}\n')
                    f.write(f'RESOURCES {blue_player.resources}\n')
                    for i in range(blue_player.units[0]):
                        f.write('WORKER STATUS BARRACKS POS\n')
                    for i in range(len(workers_disp)):
                        if workers_disp[i].team == 'blue':
                            f.write(f'WORKER STATUS {workers_disp[i].status} POS {int(workers_disp[i].x)}\n')
                    for i in range(blue_player.units[1]):
                        f.write('SWORDSMAN STATUS BARRACKS POS\n')
                    for i in range(len(swords_disp)):
                        if swords_disp[i].team == 'blue':
                            f.write(f'SWORDSMAN STATUS {swords_disp[i].status} POS {int(swords_disp[i].x)}\n')
                    for i in range(blue_player.units[2]):
                        f.write('ARCHER STATUS BARRACKS POS\n')
                    for i in range(len(archers_disp)):
                        if archers_disp[i].team == 'blue':
                            f.write(f'ARCHER STATUS {archers_disp[i].status} POS {int(archers_disp[i].x)}\n')
                    for i in range(len(archers_disp)):
                        for arrow in archers_disp[i].arrows:
                            if arrow.team == 'blue':
                                f.write(f'ARCHER_ARROW POS {int(arrow.x)} TEAM blue\n')
                    for proj in projectiles:
                        if proj.team == 'blue':
                            f.write(f'TOWER_ARROW POS {int(proj.x)} {int(proj.y)} FINAL_POS {proj.stopx} {proj.stopy}\n')
                    f.write('END Player1\n\n')
                    f.write('START Player2\n')
                    f.write(f'WALL {red_player.wall}\n')
                    f.write(f'RESOURCES {red_player.resources}\n')
                    for i in range(red_player.units[0]):
                        f.write('WORKER STATUS BARRACKS POS\n')
                    for i in range(len(workers_disp)):
                        if workers_disp[i].team == 'red':
                            f.write(f'WORKER STATUS {workers_disp[i].status} POS {int(workers_disp[i].x)}\n')
                    for i in range(red_player.units[1]):
                        f.write('SWORDSMAN STATUS BARRACKS POS\n')
                    for i in range(len(swords_disp)):
                        if swords_disp[i].team == 'red':
                            f.write(f'SWORDSMAN STATUS {swords_disp[i].status} POS {int(swords_disp[i].x)}\n')
                    for i in range(red_player.units[2]):
                        f.write('ARCHER STATUS BARRACKS POS\n')
                    for i in range(len(archers_disp)):
                        if archers_disp[i].team == 'red':
                            f.write(f'ARCHER STATUS {archers_disp[i].status} POS {int(archers_disp[i].x)}\n')
                    for i in range(len(archers_disp)):
                        for arrow in archers_disp[i].arrows:
                            if arrow.team == 'red':
                                f.write(f'ARCHER_ARROW POS {int(arrow.x)} TEAM red\n')
                    for proj in projectiles:
                        if proj.team == 'red':
                            f.write(f'TOWER_ARROW POS {int(proj.x)} {int(proj.y)} FINAL_POS {proj.stopx} {proj.stopy}\n')
                    f.write('END Player2')
                pygame.quit()

            if keys[pygame.K_SPACE]:
                # check for pause input
                if keys[pygame.K_SPACE]:
                    pause = not pause



        if blue_player.wall > 0 and red_player.wall > 0:
            if not pause:

                win.fill((255, 255, 255))

                display(win)

                # displaying the turns
                turn_txt = f'TURNS: {int(turns)}'
                turn = big_font.render(turn_txt, 1, 'black')
                win.blit(turn, (SCREEN_WIDTH/2 - big_font.size(turn_txt)[0]/2, 10))

                # displaying the team turn
                if blue_turn:
                    team_turn_txt = "Blue Team's turn"
                else:
                    team_turn_txt = "Red Team's turn"
                team_turn = big_font.render(team_turn_txt, 1, 'black')
                win.blit(team_turn, (SCREEN_WIDTH/2 - big_font.size(team_turn_txt)[0]/2, 20 + big_font.size(turn_txt)[1]))

                
                commands()

                # arrows
                for archer in archers_disp:
                    for i in range(len(archer.arrows)):
                        if i < len(archer.arrows):
                            break_bool = False
                            archer.arrows[i].update()
                            archer.arrows[i].display(win)


                            if not break_bool:
                                if archer.arrows[i].x <= 0 or archer.arrows[i].x >= SCREEN_WIDTH:
                                    archer.arrows.pop(i)
                                    break_bool = True



                            if not break_bool:
                                # check if it hit a swordsman
                                for sword in swords_disp:
                                    # if i < len(archer.arrows):
                                    if archer.arrows[i].rect.colliderect(sword.rect):
                                        if (archer.team == 'blue' and sword.team == 'red') or (archer.team == 'red' and sword.team == 'blue'):
                                            sword.health -= ARCHER_HIT
                                            archer.arrows.pop(i)
                                            break_bool = True


                            if not break_bool:
                                # check if it hit archer
                                for archer_unit in archers_disp:
                                    if i < len(archer.arrows):
                                        if archer.arrows[i].rect.colliderect(archer_unit.rect):
                                            if (archer.team == 'blue' and archer_unit.team == 'red') or (archer.team == 'red' and archer_unit.team == 'blue'):
                                                archer_unit.health -= ARCHER_HIT
                                                archer.arrows.pop(i)
                                                break_bool = True

                            if not break_bool:
                                if archer.team == 'blue':
                                    if i < len(archer.arrows):
                                        if archer.arrows[i].x >= SCREEN_WIDTH - WALL_POS:
                                            red_player.wall -= ARCHER_HIT
                                            archer.arrows.pop(i)
                                else:
                                    if i < len(archer.arrows):
                                        if archer.arrows[i].x <= WALL_POS:
                                            blue_player.wall -= ARCHER_HIT
                                            archer.arrows.pop(i)


                # projectiles
                # if blue_turn:

                opp_det = False
                break_bool = False
                
                for sword_unit in swords_disp:
                    if sword_unit.x <= WALL_POS + TOWER_RANGE and bluetower_rest == 0:
                        if sword_unit.team == 'red' and not opp_det:
                            projectiles.append(Projectile('blue', sword_unit.x, SCREEN_HEIGHT - GROUND_HEIGHT - sword_unit.rect.height))
                            opp_det = True
                            bluetower_rest += TOWER_REST

                    for proj in range(len(projectiles)):
                        if proj < len(projectiles):
                            if projectiles[proj].team == 'blue' and not break_bool and sword_unit.team == 'red':
                                if projectiles[proj].rect.colliderect(sword_unit.rect):
                                    sword_unit.health -= TOWER_HIT
                                    projectiles.pop(proj)
                                    break_bool = True
                                

                for archer_unit in archers_disp:
                    if archer_unit.x <= WALL_POS + TOWER_RANGE and bluetower_rest == 0:
                        if archer_unit.team == 'red' and not opp_det:
                            projectiles.append(Projectile('blue', archer_unit.x, SCREEN_HEIGHT - GROUND_HEIGHT - archer_unit.rect.height))
                            opp_det = True
                            bluetower_rest += TOWER_REST
                    
                    for proj in range(len(projectiles)):
                        if proj < len(projectiles):
                            if projectiles[proj].team == 'blue' and not break_bool and archer_unit.team == 'red':
                                if projectiles[proj].rect.colliderect(archer_unit.rect):
                                    archer_unit.health -= TOWER_HIT
                                    projectiles.pop(proj)
                                    break_bool = True

                # else:
   
                opp_det = False
                break_bool = False
    
                for sword_unit in swords_disp:
                    if sword_unit.x >= SCREEN_WIDTH - WALL_POS - TOWER_RANGE and redtower_rest == 0:
                        if sword_unit.team == 'blue' and not opp_det:
                            projectiles.append(Projectile('red', sword_unit.x, SCREEN_HEIGHT - GROUND_HEIGHT - sword_unit.rect.height))
                            opp_det = True
                            redtower_rest += TOWER_REST

                    for proj in range(len(projectiles)):
                        if proj < len(projectiles):
                            if projectiles[proj].team == 'red' and not break_bool and sword_unit.team == 'blue':
                                if projectiles[proj].rect.colliderect(sword_unit.rect):
                                    sword_unit.health -= TOWER_HIT
                                    projectiles.pop(proj)
                                    break_bool = True

                for archer_unit in archers_disp:
                    if archer_unit.x >= SCREEN_WIDTH - WALL_POS - TOWER_RANGE and redtower_rest == 0:
                        if archer_unit.team == 'blue' and not opp_det:
                            projectiles.append(Projectile('red', archer_unit.x, SCREEN_HEIGHT - GROUND_HEIGHT - archer_unit.rect.height))
                            opp_det = True
                            redtower_rest += TOWER_REST

                    for proj in range(len(projectiles)):
                        if proj < len(projectiles):
                            if projectiles[proj].team == 'red' and not break_bool and archer_unit.team == 'blue':
                                if projectiles[proj].rect.colliderect(archer_unit.rect):
                                    archer_unit.health -= TOWER_HIT
                                    projectiles.pop(proj)
                                    break_bool = True

                for proj in range(len(projectiles)):
                    if proj < len(projectiles):
                        projectiles[proj].update()
                        projectiles[proj].display(win)

                        if projectiles[proj].x <= projectiles[proj].stopx + 3 and projectiles[proj].x >= projectiles[proj].stopx - 3 \
                            and projectiles[proj].y <= projectiles[proj].stopy + 3 and projectiles[proj].y >= projectiles[proj].stopy - 3:
                            projectiles.pop(proj)


                # blue wall health
                ind = 0
                for i in range(int(blue_player.wall/5)):
                    pygame.draw.rect(win, 'green', (i + WALL_POS - 50, SCREEN_HEIGHT - WALL_HEIGHT - 20, 1, 10))
                    ind = i

                while ind < 99:
                    pygame.draw.rect(win, 'red', (ind + WALL_POS - 50, SCREEN_HEIGHT - WALL_HEIGHT - 20, 1, 10))
                    ind += 1
                
                
                # red wall health
                ind = 0
                for i in range(int(red_player.wall/5)):
                    pygame.draw.rect(win, 'green', (i + SCREEN_WIDTH - WALL_POS - 50, SCREEN_HEIGHT - WALL_HEIGHT - 20, 1, 10))
                    ind = i

                while ind < 99:
                    pygame.draw.rect(win, 'red', (ind + SCREEN_WIDTH - WALL_POS - 50, SCREEN_HEIGHT - WALL_HEIGHT - 20, 1, 10))
                    ind += 1

                for worker_unit in workers_disp:
                    worker_unit.update()

                for sword in swords_disp:
                    sword.update()

                for archer in archers_disp:
                    archer.update()

                if pygame.time.get_ticks() - turn_time >= 4000:
                    update()

            else:

                win.fill((255, 255, 255))

                display(win)

                # displaying the turns
                turn_txt = f'TURNS: {int(turns)}'
                turn = big_font.render(turn_txt, 1, 'black')
                win.blit(turn, (SCREEN_WIDTH/2 - big_font.size(turn_txt)[0]/2, 10))

                pause_text = 'Paused'
                paused = big_font.render(pause_text, 1, 'black')
                win.blit(paused, (SCREEN_WIDTH/2 - big_font.size(pause_text)[0]/2, 20 + big_font.size(turn_txt)[1]))

            pygame.display.update()

        
        
        else:
            if blue_player.wall == 0:
                print('Red wins')
            elif red_player.wall == 0:
                print('Blue wins')
            run = False