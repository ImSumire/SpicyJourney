import pygame


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera Offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Box set
        self.camera_borders = {
            "left": width // 2.2,
            "right": width // 2.2,
            "top": height // 2.2,
            "bottom": height // 2.2,
        }
        l = self.camera_borders["left"]
        t = self.camera_borders["top"]
        w = self.display_surface.get_size()[0] - (
            self.camera_borders["left"] + self.camera_borders["right"]
        )
        h = self.display_surface.get_size()[1] - (
            self.camera_borders["top"] + self.camera_borders["bottom"]
        )
        self.camera_rect = pygame.Rect(l, t, w, h)

        # Zoom
        self.zoom_scale = 4
        self.internal_surf_size = (width / 2, height / 2)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(
            center=(self.half_w, self.half_h)
        )
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    # Follow player
    def centered_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    # Box
    def box_camera(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders["left"]
        self.offset.y = self.camera_rect.top - self.camera_borders["top"]

    def draw(self, player):

        self.centered_camera(player)
        # self.box_camera(player)

        self.internal_surf.fill((0, 0, 0))

        # Ground
        # ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        # self.internal_surf.blit(self.ground_surf,ground_offset)

        # Active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.internal_surf.blit(
                sprite.image, sprite.rect.topleft - self.offset + self.internal_offset
            )

        scaled_surf = pygame.transform.scale(
            self.internal_surf,
            [
                int(self.internal_surface_size_vector[0] * 4),
                int(self.internal_surface_size_vector[1] * 4),
            ],
        )
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)