/*
 * Utilities to safely intepret the DB input
 * Throws on badly formatted data
*/
#include "dbsafeutils.hpp"

using namespace std;

namespace dbquery {

DBSafeUtils::DBSafeUtils(void)
{
}

DBSafeUtils::~DBSafeUtils(void)
{
}

void DBSafeUtils::safeToInt(int * integer, const pqxx::field & fieldValue)
{
	checkValidInput(fieldValue.c_str(), REGEX_SIGNED_INT);
	toInt(integer, fieldValue);
}

void DBSafeUtils::safeToString(string * str, const pqxx::field & fieldValue)
{
	checkValidInput(fieldValue.c_str(), REGEX_BASIC_STRING);
	toString(str, fieldValue);
}

void DBSafeUtils::safeToString(string * str, const pqxx::field & fieldValue, const regex & regexExpression)
{
	checkValidInput(fieldValue.c_str(), regexExpression);
	toString(str, fieldValue);
}


/*
 * Functions to throw DBExceptionBadData on bad input
 */
void DBSafeUtils::checkValidInput(const char * input, const regex & regexExpression)
{
	bool matchResult = regex_match(input, regexExpression);
	if (matchResult != true)
	{
		throw DBExceptionBadData();
	}
}

void DBSafeUtils::checkValidInput(const string & input, const regex & regexExpression)
{
	bool matchResult = regex_match(input, regexExpression);
	if (matchResult != true)
	{
		throw DBExceptionBadData();
	}
}

}
