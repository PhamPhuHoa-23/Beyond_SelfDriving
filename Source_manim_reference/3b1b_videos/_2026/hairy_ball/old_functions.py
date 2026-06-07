from manim_imports_ext import *

def sanitize_3D_vector(pt):
    pts = np.array(pt, ndmin=2)
    if len(pts.shape) > 2:
        raise ValueError('3D vectors cannot have depth more than 2.')
    if pts.shape[1] != 3:
        raise ValueError('3D vectors must have 3 components.')
    return pts

def sanitize_scalar(x):
    x_array = np.array(x, ndmin=1)
    if len(x_array.shape) > 1:
        raise ValueError('Scalars cannot have depth more than 2.')
    return x_array

def direction_field(pt, discontinuities='equator', epsilon=0.01):
    pts = sanitize_3D_vector(pt)
    x, y, z = np.transpose(pts)
    if discontinuities == 'equator':
        mask = abs(z) < 0.1
        equator = np.stack((-y, x, 0 * z))
        non_equator = np.stack((0 * x, z, -y))
        perp = mask * equator + np.logical_not(mask) * non_equator
    elif discontinuities == 'two':
        mask = abs(abs(z) - 1) < epsilon
        poles = np.stack((0 * x, z, -y))
        non_poles = np.stack((-y, x, 0 * z))
        perp = mask * poles + np.logical_not(mask) * non_poles
    elif discontinuities == 'one':
        mask = abs(z - 1) < epsilon
        north_pole = np.stack((0 * x, z, -y))
        X = x ** 2 - y ** 2 - (z - 1) ** 2
        Y = 2 * x * y
        Z = 2 * x * (z - 1)
        non_north_pole = np.stack((X, Y, Z))
        perp = mask * north_pole + np.logical_not(mask) * non_north_pole
    else:
        raise NotImplementedError()
    field = np.transpose(perp)
    num_pts = field.shape[0]
    norm = np.linalg.norm(field, axis=1)
    norm = np.reshape(norm, [num_pts, 1])
    vec = field / norm
    return vec

def distension(pt, t):
    time_factor = np.sin(np.pi * t)
    x, y, z = np.transpose(pt)
    space_factor = y * z
    rho_factor = np.tensordot(time_factor, space_factor, axes=0)
    return rho_factor

def great_circle_map(pt, t, discontinuities='one', distend=0, epsilon=0.01):
    times = sanitize_scalar(t)
    dist_factors = sanitize_scalar(distend)
    pts = sanitize_3D_vector(pt)
    units = direction_field(pts, discontinuities, epsilon)
    scaled_times = np.pi * times
    u1 = np.cos(scaled_times)
    u2 = np.sin(scaled_times)
    base_pts = np.tensordot(u1, pts, axes=0) + np.tensordot(u2, units, axes=0)
    rho_factors = distension(pts, times)
    full_factors = 1 + np.tensordot(rho_factors, dist_factors, axes=0)
    base_pts_reshaped = np.expand_dims(base_pts, axis=2)
    factors_reshaped = np.expand_dims(full_factors, axis=-1)
    new_pts = base_pts_reshaped * factors_reshaped
    new_pts = new_pts.transpose((0, 2, 1, 3))
    return new_pts

def test_direction_field(num_pts=1000, epsilon=0.001):
    points = fibonacci_sphere(num_pts)
    failed_counts = {'equator': 0, 'two': 0, 'one': 0}
    for disc in ['equator', 'two', 'one']:
        field = direction_field(points, discontinuities=disc, epsilon=epsilon)
        dots = (points * field).sum(axis=1)
        failures = (abs(dots) >= epsilon).sum(axis=0)
        failed_counts[disc] = failures
    print('Number of points where the direction field failed to be orthogonal to the sphere.')
    print('')
    for key in failed_counts.keys():
        value = failed_counts[key]
        print(f'{key}: {value} points')
    print('')
    print('Count completed.')
    return None

def test_great_circle_map(discontinuities='one'):
    epsilon = 1e-06
    pts = fibonacci_sphere(15)
    distends = [0.1 * x for x in range(11)]
    end_pts = great_circle_map(pts, [0, 1], discontinuities=discontinuities, distend=distends)
    pts_dims = end_pts.shape
    if len(pts_dims) != 4:
        print('Warning! Array has an incorrect number of dimensions.')
    elif pts_dims != (2, len(distends), len(pts), 3):
        print('Warning: Dimensions of array are incorrect.')
    else:
        print('Array has expected dimensions.')
        print('')
    beginning = end_pts[0]
    ending = end_pts[1]
    identity_pass = True
    antipode_pass = True
    for distend, pts_copy in zip(distends, beginning):
        if np.linalg.norm(pts - pts_copy) > epsilon:
            if identity_pass:
                print('Warning! At time t=0, non-identity map at distensions:')
            identity_pass = False
            print(distend)
    if identity_pass:
        print('Homotopy correctly defaults to identity at time t=0')
        print('No dependence on distension')
    print('')
    for distend, pts_copy in zip(distends, ending):
        if np.linalg.norm(pts + pts_copy) > epsilon:
            if antipode_pass:
                print('Warning! At time t=1, non-antipode map at distensions:')
            antipode_pass = False
            print(distend)
    if antipode_pass:
        print('Homotopy correctly defaults to antipode at time t=1')
        print('No dependence on distension')
    print('')
    halfway_pts = great_circle_map(pts, 1 / 2, discontinuities=discontinuities)[0][0]
    distances = np.linalg.norm(halfway_pts - pts, axis=1)
    discrepancies = np.abs(distances - np.sqrt(2))
    if np.max(discrepancies) > epsilon:
        print('Warning! Points tested at the halfway point at zero distension are in the wrong position.')
    else:
        print('Points are halfway around the great circle at t=1/2 with distension 0.')
    print('')
    infinitesimal_pts = great_circle_map(pts, epsilon ** 2, discontinuities=discontinuities)[0][0]
    velocities_actual = infinitesimal_pts - beginning[0]
    units = direction_field(pts, discontinuities=discontinuities)
    velocities_expected = units * np.pi * epsilon ** 2
    velocity_discrepancy = np.linalg.norm(velocities_actual - velocities_expected, axis=1)
    if np.max(velocity_discrepancy) > epsilon:
        print('Warning! Points do not appear to move in the direction of the vector field.')
    else:
        print('Points move in the direction of the vector field.')
    print('')
    times = np.random.rand(5)
    distension_pts = great_circle_map(pts, times, discontinuities=discontinuities, distend=distends)
    zero_distension_pts = distension_pts[0:, 0:1, 0:, 0:]
    norms = np.expand_dims(np.linalg.norm(distension_pts, axis=-1), axis=-1)
    normalized_pts = distension_pts / norms
    differences = normalized_pts - zero_distension_pts
    discrepancies = np.linalg.norm(differences, axis=-1)
    if np.max(discrepancies) > epsilon:
        print('Warning! Discrepancy is shifting the directions of points, not just radially.')
    else:
        print('Discrepancy moves points only radially.')
    print('')
    print('All tests completed.')
    return None

def spherical_surface(theta, phi):
    X = np.sin(phi) * np.cos(theta)
    Y = np.sin(phi) * np.sin(theta)
    Z = np.cos(phi)
    return np.array([[X, Y, Z]])

def spherical_eversion(theta, phi, t):
    pt = spherical_surface(theta, phi)
    new_pt = great_circle_map(pt, t, discontinuities='one', distend=0.5)
    return new_pt[0][0][0]