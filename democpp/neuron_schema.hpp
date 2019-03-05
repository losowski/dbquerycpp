#ifndef NEURON_SCHEMA_HPP
#define NEURON_SCHEMA_HPP

#include "dbconnection.hpp"

#include "tbody.hpp"
#include "tindividual.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

class NeuronSchema : public dbquery::DBConnection
{
	public:
		NeuronSchema(const string & connection);
		~NeuronSchema(void);
	public:
		//void connect(void);
		//tBody
		ptBody gtBody(int primaryKey);
		//tIndividual
		ptIndividual gtIndividual(int primaryKey);
		//TODO: Add means to get all tIndividuals for a particular tBody key
		paptIndividual gtIndividualbytBody(const tBody & body);
};
}
#endif //NEURON_SCHEMA_HPP
