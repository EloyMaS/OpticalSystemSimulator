import numpy as np
import matplotlib.pyplot as plt


class OpticalSystem:
    '''This class contains methods that modify the characteristics of the optical system
    '''

    def __init__(self):
        self.S = np.array([[1, 0],
                           [0, 1]])
        self.element_details = []
        self.diaphragm_details = []

        try:
            self.n = float(input('Introduzca el índice de refracción del medio ' \
                                 'principal:'))
        except Exception as e:
            print(e)

    def add_thin_lens(self):
        try:
            if not self.element_details:
                x = 0.
            else:
                x = float(input('Introduzca la posición de la lente:'))

            diameter = float(input('Introduzca el diámetro de la lente:'))
            fi = float(input('Introduzca la distancia focal imagen de la lente:'))
            S = np.array([[1, 0],
                          [-1 / fi, 1]])

            self._append_element_details(diameter, x, S, 'thin_lens')

        except Exception as e:
            print(e)

    def add_thick_lens(self):
        try:
            if not self.element_details:
                x = 0.

            else:
                x = float(input('Introduzca la posición de la lente ' \
                                '(vértice de la primera superficie):'))

            diameter = float(input('Introduzca el diámetro de la lente:'))
            R1 = float(input('''Introduzca el radio de la primera superficie ''' \
                             '''(introduzca 'plano' si la superficie es plana):'''))
            R2 = float(input('''Introduzca el radio de la segunda superficie ''' \
                             '''(introduzca 'plano' si la superficie es plana):'''))
            thickness = float(input('Introduzca el grosor de la lente:'))
            n2 = float(input('Introduzca el coef. de refracción del medio interior:'))

            if R1 == 'plano':
                mR1 = np.array([[1, 0],
                                [0, n2 / self.n]])

            elif type(R1) == float:
                mR1 = np.array([[1, 0],
                                [(self.n - n2) / (R1 * n2), self.n / n2]])

            else:
                raise ValueError('Invalid entry for R1')

            mT = np.array([[1, thickness],
                           [0, 1]])

            if R2 == 'plano':
                mR2 = np.array([[1, 0],
                                [0, n2 / self.n]])

            elif type(R1) == float:
                mR2 = np.array([[1, 0],
                                [-(self.n - n2) / (R2 * self.n), n2 / self.n]])

            else:
                raise ValueError('EntryError: Invalid entry for R1')

            matrix = np.matmul(mT, mR1)
            matrix = np.matmul(mR2, matrix)

            self._append_element_details(diameter, x, matrix, 'thick_lens')

        except Exception as e:
            print(e)

    def add_flat_mirror(self):
        try:

            if not self.element_details:
                x = 0.

            else:
                x = float(input('Introduzca la posición del espejo:'))

            diameter = float(input('Introduzca el diámetro del espejo:'))

            R = np.array([[1, 0],
                          [0, -1]])

            self._append_element_details(diameter, x, R, 'flat_mirror')

        except Exception as e:
            print(e)

    def add_spherical_mirror(self):
        try:

            if not self.element_details:
                x = 0.

            else:
                x = float(input('Introduzca la posición del espejo:'))

            diameter = float(input('Introduzca el diámetro del espejo:'))
            radius = float(input('Introduzca el radio de curvatrua del espejo:'))

            R = np.array([[1, 0],
                          [2 / radius, -1]])

            self._append_element_details(diameter, x, R, 'spherical_mirror')

        except Exception as e:
            print(e)

    def add_diaphragm(self):
        try:
            x = float(input('Introduzca la posición del diafragma:'))
            diameter = float(input('Introduzca el diámetro del diafragma:'))
            matrix = np.array([[1, 0],
                               [0, 1]])
            self._append_element_details(diameter, x, matrix, 'diaphragm')

        except Exception as e:
            print(e)

    def _append_element_details(self, _d, _x, matrix, element_type):
        detail_dict = dict()
        detail_dict['diameter'], detail_dict['position'] = _d, _x
        detail_dict['matrix'], detail_dict['type'] = matrix, element_type
        self.element_details.append(detail_dict)

    def _sort(self, element):
        return element['position']


class Projection(OpticalSystem):
    '''This class contains the ray_trace method that models the behavior of a ray that enters the systems with a height
        _h and an incidence angle _sigma
    '''

    def __init__(self):
        super(Projection, self).__init__()

    def ray_trace(self, _h, _sigma):
        self.h = _h
        self.sigma = _sigma
        vector = np.array([_h, _sigma])
        self.element_details.sort(key=self._sort)

        if self.element_details:

            for i, element in enumerate(self.element_details):
                # print(vector)
                if element['type'] == 'diaphragm':

                    if element['diameter'] / 2 <= abs(vector[0]):
                        return 'El rayo se detiene en el diafragma con posición ' \
                               f'''{element['position']}'''

                else:

                    if (element['diameter'] / 2 >= vector[0]) and (-element['diameter'] / 2 <= vector[0]):
                        vector = element['matrix'] @ vector

                if i < len(self.element_details) - 1:
                    distance = self.element_details[i + 1]['position'] - element['position']
                    vector = np.array([[1, -distance], [0, 1]]) @ vector

            return vector

        else:
            raise ValueError('El sistema no contiene elementos')
