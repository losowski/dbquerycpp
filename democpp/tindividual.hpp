#ifndef NEURON_SCHEMA_TINDIVIDUAL_HPP
#define NEURON_SCHEMA_TINDIVIDUAL_HPP

#include <memory>
#include <vector>

#include "dbresult.hpp"
#include "dbsafeutils.hpp"

#include "tbody.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

class tIndividual;

typedef shared_ptr<tIndividual> ptIndividual;
typedef vector < ptIndividual >  aptIndividual;
typedef shared_ptr < aptIndividual>  paptIndividual;

class tIndividual : public DBResult
{
	public:
		static const string SQL_SELECT;
	public:
		tIndividual(dbquery::DBConnection * connection);
		tIndividual(dbquery::DBConnection * connection, const int primaryKey);
		tIndividual(dbquery::DBConnection * connection, int id, int body_id, string & name);
		~tIndividual(void);
	public:
		//SELECT
		void selectRowSQL(shared_ptr<pqxx::work> txn);
		//DELETE
		void deleteRowSQL(shared_ptr<pqxx::work> txn);
		//UPDATE
		void updateRowSQL(shared_ptr<pqxx::work> txn);
		//INSERT
		void insertRowSQL(shared_ptr<pqxx::work> txn);
		//Schema Functions
		shared_ptr<tBody> gtBody(void);
		static paptIndividual gtIndividualsFromBody(dbquery::DBConnection * connection, const tBody & body);
	public:
		int 		id;
		int 		body_id;
		string		name;
};
}
#endif //NEURON_SCHEMA_TINDIVIDUAL_HPP
