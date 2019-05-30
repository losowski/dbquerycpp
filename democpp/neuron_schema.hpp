#ifndef NEURON_SCHEMA_HPP
#define NEURON_SCHEMA_HPP

#include <map>
#include <memory>

#include "dbconnection.hpp"
#include "dbtransaction.hpp"

#include "tbody.hpp"
#include "tindividual.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

typedef map < int , ptBody > maptBody;
typedef	map < int , ptIndividual > maptIndividual;

class NeuronSchema : public dbquery::DBConnection
{
	public:
		NeuronSchema(const string & connection);
		~NeuronSchema(void);
	public:
		//void connect(void);
		//--
		//tBody
		ptBody gtBody(int primaryKey);
		ptBody gtBody(int id, const string & text);
		paptBody gtBodyName(string & name);
		//--
		//tIndividual
		ptIndividual gtIndividual(int primaryKey);
		ptIndividual gtIndividual(int id, int body_id, string & name);
		//TODO: Add means to get all tIndividuals for a particular tBody key
		paptIndividual gtIndividualbytBody(const tBody & body);
	public:
		DBTransaction		transaction;
	private:
		maptBody			tBodyMap;
		maptIndividual		tIndividualMap;
};

}
#endif //NEURON_SCHEMA_HPP
