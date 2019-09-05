#ifndef EMA_HPP_
#define EMA_HPP_

#include <cmath>
#include <boost/python.hpp>

/**
 * Calcula el error medio absoluto en porcentaje entre una colección de observaciones y de predicciones.
 *
 * @return 0 si las observaciones suman 0. El error medio absoluto en porcentaje en caso contrario.
 */
template<typename forward_iterator_observaciones,
		typename forward_iterator_predicciones>
double ema(forward_iterator_observaciones observaciones,
		forward_iterator_observaciones observaciones_fin,
		forward_iterator_predicciones predicciones) {
	double error_acumulado = 0.;
	double observacion_total = 0.;

	for (; observaciones != observaciones_fin;
			++observaciones, ++predicciones) {
		error_acumulado += std::abs(*observaciones - *predicciones);
		observacion_total += *observaciones;
	}

	if (observacion_total < 1e-7) {
		return 0.;
	}

	return (error_acumulado / observacion_total) * 100.;
}

#endif /* EMA_HPP_ */

BOOST_PYTHON_MODULE(EMA_c)
{
    using namespace boost::python;
    def("ema", ema);
}
