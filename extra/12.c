#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
	JSON object types
*/

typedef enum Type {
	STRING, NUMBER, OBJECT, ARRAY
} Type;

typedef struct ArrayElem* Array;

typedef struct ObjectElem* Object;

typedef const char* String;

typedef int Number;

typedef struct Value {
	Type type;
	union {
		Array array;
		Object object;
		String string;
		Number number;
	};
} Value;

typedef struct ArrayElem {
	struct ArrayElem *next;
	Value value;
} ArrayElem;

typedef struct ObjectElem {
	struct ObjectElem *next;
	String key;
	Value value;
} ObjectElem;

/*
	JSON parsing functions
*/

const char* ParseValue(const char* p, Value* value);

const char* ParseString(const char* p, String* string) {
	if (*p++ != '"') return NULL;
	const char* q = p;
	while (*q != '"') if (*q++ == '\0') return NULL;
	*string = strndup(p, q - p);
	return ++q;
}

const char* ParseNumber(const char* p, Number* number) {
	bool neg = false;
	if (*p == '-') neg = true, ++p;
	*number = 0;
	if (*p == '0') return ++p;
	if (*p < '1' || *p > '9') return NULL;
	do {
		*number = 10 * *number + (*p++ - '0');
	} while (*p >= '0' && *p <= '9');
	if (neg) *number = -*number;
	return p;
}

const char* ParseObject(const char* p, Object* object) {
	if (*p++ != '{') return NULL;
	*object = NULL;
	if (*p == '}') return ++p;
	for (;;) {
		*object = malloc(sizeof(ObjectElem));
		if ((p = ParseString(p, &(*object)->key)) == NULL) return NULL;
		if (*p++ != ':') return NULL;
		if ((p = ParseValue(p, &(*object)->value)) == NULL) return NULL;
		(*object)->next = NULL;
		object = &(*object)->next;
		if (*p == '}') return ++p;
		if (*p++ != ',') return NULL;
	}
}

const char* ParseArray(const char* p, Array* array) {
	if (*p++ != '[') return NULL;
	*array = NULL;
	if (*p == ']') return ++p;
	for (;;) {
		*array = malloc(sizeof(ArrayElem));
		if ((p = ParseValue(p, &(*array)->value)) == NULL) return NULL;
		(*array)->next = NULL;
		array = &(*array)->next;
		if (*p == ']') return ++p;
		if (*p++ != ',') return NULL;
	}
}

const char* ParseValue(const char* p, Value* value) {
	const char* q;
	if ((q = ParseString(p, &value->string)) != NULL) {
		value->type = STRING;
		return q;
	}
	if ((q = ParseNumber(p, &value->number)) != NULL) {
		value->type = NUMBER;
		return q;
	}
	if ((q = ParseObject(p, &value->object)) != NULL) {
		value->type = OBJECT;
		return q;
	}
	if ((q = ParseArray(p, &value->array)) != NULL) {
		value->type = ARRAY;
		return q;
	}
	return NULL;
}

/*
	JSON printing functions (useful for debugging)
*/

void PrintValue(Value value, FILE *fp);

void PrintString(String string, FILE *fp) {
	fprintf(fp, "\"%s\"", string);
}

void PrintNumber(Number number, FILE *fp) {
	fprintf(fp, "%d", number);
}

void PrintObject(Object object, FILE *fp) {
	fputc('{', fp);
	for (ObjectElem* elem = object; elem != NULL; elem = elem->next) {
		if (elem != object) fputc(',', fp);
		PrintString(elem->key, fp);
		fputc(':', fp);
		PrintValue(elem->value, fp);
	}
	fputc('}', fp);
}

void PrintArray(Array array, FILE* fp) {
	fputc('[', fp);
	for (ArrayElem* elem = array; elem != NULL; elem = elem->next) {
		if (elem != array) fputc(',', fp);
		PrintValue(elem->value, fp);
	}
	fputc(']', fp);
}

void PrintValue(Value value, FILE *fp) {
	switch (value.type) {
	case STRING: PrintString(value.string, fp); break;
	case NUMBER: PrintNumber(value.number, fp); break;
	case OBJECT: PrintObject(value.object, fp); break;
	case ARRAY: PrintArray(value.array, fp); break;
	}
}

/*
	Main solution
*/

int Calculate(Value value, const char* forbidden) {
	int result = 0;
	switch (value.type) {
	case NUMBER:
		result = value.number;
		break;
	case OBJECT:
		for (ObjectElem* elem = value.object; elem != NULL; elem = elem->next) {
			if (forbidden != NULL && elem->value.type == STRING && strcmp(forbidden, elem->value.string) == 0) return 0;
			result += Calculate(elem->value, forbidden);
		}
		break;
	case ARRAY:
		for (ArrayElem* elem = value.array; elem != NULL; elem = elem->next) {
			result += Calculate(elem->value, forbidden);
		}
		break;
	default: break;
	}
	return result;
}

int main() {
	static char buffer[1 << 20];
	fgets(buffer, sizeof(buffer), stdin);
	Value value;
	if (ParseValue(buffer, &value) == NULL) {
		fprintf(stderr, "Failed to parse JSON from stdin!\n");
		return 1;
	}
	printf("%d\n", Calculate(value, NULL));
	printf("%d\n", Calculate(value, "red"));
	return 0;
}
