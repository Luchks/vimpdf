# Inventario de entorno — Linux

## Plataforma

- Plataforma: Linux x64
- Distribución: Arch Linux
- Release: rolling
- Kernel: 7.2.2-arch1-1
- Arquitectura: x86_64
- Sesión gráfica: Wayland

## CPU

- Modelo: AMD Ryzen 5 5600H with Radeon Graphics
- Núcleos físicos: 6
- Hilos: 12
- Virtualización: AMD-V

## GPU

- GPU dedicada: NVIDIA Corporation GA107M [GeForce RTX 3050 Mobile]
- GPU integrada: AMD/ATI Cezanne [Radeon Vega Series / Radeon Vega Mobile Series]

## Monitor

- Salida: eDP-1
- Fabricante: Lenovo Group Limited
- Resolución activa: 1920x1080
- Frecuencia activa: 120.002 Hz
- Escala: 1
- Formato: XRGB8888
- VRR: false

## Teclado

- Layout: us
- Keymap activo: English (US)
- Layout index: 0

## Filesystem del producto

- Ruta del producto: /home/luchks/vimpdf
- Filesystem: ext4
- Dispositivo: /dev/nvme1n1p3
- Punto de montaje: /
- Opciones observadas: rw,relatime

## Estado de plataforma

Linux: disponible.

Windows: BLOCKED.

Motivo de Windows BLOCKED: no se dispone de evidencia necesaria de una plataforma Windows x64 real para ejecutar las tareas correspondientes. BLOCKED no constituye un veredicto técnico de rechazo.

## Responsable de decisión

El responsable de las decisiones de backlog es el usuario.

## Glosario de veredictos

- APROBADO: todos los requisitos [E] aplicables satisfechos y no quedan TBD que afecten al requisito.
- APROBADO CON LIMITACIONES: todos los [E] satisfechos, con limitaciones explícitas, acotadas y aceptadas en el informe.
- RECHAZADO: al menos un requisito [E] aplicable no satisfecho.
- BLOCKED: no existe evidencia necesaria por falta de una plataforma, entrada o prerrequisito, y no constituye por sí mismo un veredicto técnico sobre el candidato.

## Evidencia

Comandos utilizados:

- `cat /etc/os-release`
- `uname -r`
- `echo $XDG_SESSION_TYPE`
- `lscpu`
- `lspci | grep -Ei 'vga|3d|display'`
- `hyprctl monitors`
- `hyprctl devices`
- `lsblk -f`
- `findmnt -T .`
- `localectl status`
