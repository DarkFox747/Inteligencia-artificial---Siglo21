import numpy as np
import matplotlib.pyplot as plt

def generate_test_image(width=200, height=200):
    """
    Genera una imagen binaria simple con dos líneas brillantes
    sobre fondo oscuro: una horizontal y una diagonal.
    """
    img = np.zeros((height, width), dtype=np.uint8)

    # Línea horizontal en el centro
    img[height // 2, 20:180] = 255

    # Línea diagonal desde abajo-izquierda hacia arriba-derecha
    for i in range(40, 160):
        y = height - i - 1
        x = i
        if 0 <= y < height and 0 <= x < width:
            img[y, x] = 255

    return img

def hough_lines(binary_img, theta_res=1, rho_res=1):
    """
    Implementación simple de la transformada de Hough para rectas.

    Parámetros
    ----------
    binary_img : np.ndarray (2D)
        Imagen binaria (bordes = píxeles no nulos).
    theta_res : float
        Resolución angular en grados para theta.
    rho_res : float
        Resolución en píxeles para rho.

    Retorna
    -------
    accumulator : np.ndarray
        Matriz acumuladora de Hough (rho x theta).
    thetas : np.ndarray
        Vector de valores de theta (en radianes).
    rhos : np.ndarray
        Vector de valores de rho.
    """
    height, width = binary_img.shape

    # Theta en grados: de -90 a 90 (sin incluir 90 para mantener longitud pareja)
    thetas = np.deg2rad(np.arange(-90.0, 90.0, theta_res))

    # Longitud máxima posible de rho (diagonal de la imagen)
    diag_len = int(np.ceil(np.sqrt(width * width + height * height)))
    rhos = np.arange(-diag_len, diag_len + 1, rho_res)

    # Acumulador: filas = rhos, columnas = thetas
    accumulator = np.zeros((len(rhos), len(thetas)), dtype=np.uint64)

    # Índices de los píxeles de borde (y, x)
    y_idxs, x_idxs = np.nonzero(binary_img)

    # Votación en el acumulador
    for x, y in zip(x_idxs, y_idxs):
        for theta_idx, theta in enumerate(thetas):
            rho = int(round(x * np.cos(theta) + y * np.sin(theta)))
            rho_idx = rho + diag_len  # desplazamos para que el índice sea >= 0
            accumulator[rho_idx, theta_idx] += 1

    return accumulator, thetas, rhos

def find_peaks(accumulator, thetas, rhos, threshold, min_distance=10):
    """
    Busca picos en el acumulador de Hough por encima de un umbral.
    Aplica supresión de no-máximos para evitar detecciones duplicadas.

    Parámetros
    ----------
    min_distance : int
        Distancia mínima entre picos en el espacio de Hough.

    Retorna una lista de pares (rho, theta) ordenados por votos.
    """
    peaks = []
    num_rhos, num_thetas = accumulator.shape
    
    # Crear una copia del acumulador para ir marcando zonas procesadas
    acc_copy = accumulator.copy()

    # Buscar picos ordenados por número de votos
    while True:
        # Encontrar el máximo actual
        max_val = acc_copy.max()
        
        if max_val < threshold:
            break
            
        # Encontrar la posición del máximo
        max_pos = np.unravel_index(acc_copy.argmax(), acc_copy.shape)
        rho_idx, theta_idx = max_pos
        
        # Guardar el pico
        rho = rhos[rho_idx]
        theta = thetas[theta_idx]
        peaks.append((rho, theta, max_val))
        
        # Suprimir región alrededor del pico para evitar duplicados
        rho_min = max(0, rho_idx - min_distance)
        rho_max = min(num_rhos, rho_idx + min_distance + 1)
        theta_min = max(0, theta_idx - min_distance)
        theta_max = min(num_thetas, theta_idx + min_distance + 1)
        
        acc_copy[rho_min:rho_max, theta_min:theta_max] = 0

    return peaks

def plot_results(img, accumulator, thetas, rhos, peaks):
    """
    Muestra:
    - la imagen original con las rectas detectadas
    - el acumulador de Hough
    """
    fig, (ax_img, ax_acc) = plt.subplots(1, 2, figsize=(12, 5))

    # Imagen original
    ax_img.imshow(img, cmap='gray')
    ax_img.set_title(f"Imagen original - {len(peaks)} líneas detectadas")
    ax_img.set_axis_off()

    # Dibujar las rectas detectadas
    height, width = img.shape
    colors = plt.cm.rainbow(np.linspace(0, 1, len(peaks)))
    
    for idx, (rho, theta, votes) in enumerate(peaks):
        # Ecuación de la recta: x cos(theta) + y sin(theta) = rho
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho

        # Dos puntos alejados sobre la recta (para trazarla completa)
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        ax_img.plot((x1, x2), (y1, y2), linewidth=2, color=colors[idx], 
                   label=f'L{idx+1}: ρ={rho:.1f}, θ={np.rad2deg(theta):.1f}°, votos={votes}')

    if peaks:
        ax_img.legend(loc='upper right', fontsize=8)

    # Acumulador de Hough
    extent = [np.rad2deg(thetas[0]), np.rad2deg(thetas[-1]), rhos[-1], rhos[0]]
    ax_acc.imshow(accumulator, cmap='hot', aspect='auto', extent=extent)
    ax_acc.set_title("Acumulador de Hough")
    ax_acc.set_xlabel("θ (grados)")
    ax_acc.set_ylabel("ρ (píxeles)")
    
    # Marcar los picos en el acumulador
    for rho, theta, votes in peaks:
        ax_acc.plot(np.rad2deg(theta), rho, 'cx', markersize=10, markeredgewidth=2)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 1. Generar imagen de prueba
    img = generate_test_image()

    # 2. En este ejemplo la imagen ya es binaria
    binary_img = img

    # 3. Aplicar transformada de Hough
    print("Aplicando transformada de Hough...")
    accumulator, thetas, rhos = hough_lines(binary_img,
                                            theta_res=1,
                                            rho_res=1)

    # 4. Buscar picos en el acumulador
    # Ajustar el umbral según el tamaño de las líneas
    print("Buscando líneas en el acumulador...")
    peaks = find_peaks(accumulator, thetas, rhos, threshold=80, min_distance=10)
    
    print(f"\nSe detectaron {len(peaks)} líneas:")
    for idx, (rho, theta, votes) in enumerate(peaks):
        print(f"  Línea {idx+1}: ρ={rho:.2f} píxeles, θ={np.rad2deg(theta):.2f}°, votos={votes}")

    # 5. Visualizar resultados
    plot_results(img, accumulator, thetas, rhos, peaks)
