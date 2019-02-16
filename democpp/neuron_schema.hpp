#ifndef NEURON_SCHEMA_HPP
#define NEURON_SCHEMA_HPP

#include <string>
#include <list>
#include <map>
#include <set>
#include <tuple>

#include "dbconnection.hpp"

#include "tbody.hpp"
#include "tindividual.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

typedef set < shared_ptr<tIndividual> > tIndividuals_t;

class NeuronSchema : public dbquery::DBConnection
{
	public:
		NeuronSchema(const string & connection);
		~NeuronSchema(void);
	public:
		//void connect(void);
		//tBody
		shared_ptr<tBody> gtBody(int primaryKey);
		//tIndividual
		shared_ptr<tIndividual> gtIndividual(int primaryKey);
		//TODO: Add means to get all tIndividuals for a particular tBody key
		aptIndividual gtIndividualbytBody(const tBody & body);
	protected:
		shared_ptr <tIndividuals_t> tIndividualbytBody;
};
}
#endif //NEURON_SCHEMA_HPP
