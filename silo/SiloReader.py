from pypion.ReadData import ReadData
import numpy as np




class GetSiloData(ReadData):

    def get_basic_data(self):
        '''
        return basic data
        :return:
        '''
        basic = self.get_1Darray("Density")
        return {'sim_time':basic['sim_time'],
                'min_extents':basic['min_extents'],
                'max_extents':basic['max_extents']}



    def get_radial_coordinate(self):
        '''
        This function returns the radial coordinate array
        '''

        dim_min_level = self.get_basic_data()['min_extents']
        dim_max_level = self.get_basic_data()['max_extents']
        # we have just one level
        first_level_min = dim_min_level[0]
        first_level_max = dim_max_level[0]
        rmin = first_level_min[0]
        rmax = first_level_max[0]
        n_radial_grids = self.ngrid()[0]
        dr = (rmax - rmin) / n_radial_grids
        r0 = rmin + 0.5 * dr
        rn = rmax - 0.5 * dr
        radial_coordinate = np.linspace(r0, rn, n_radial_grids)
        return radial_coordinate

    def get_parameter(self, Parameter):
        '''
        :param Parameter: Any physical quantities
        :return: data corresponding to the parameter
        '''
        parameter_level = self.get_1Darray(Parameter)['data']
        parameter_first_level = parameter_level[0]
        return np.array(parameter_first_level)









