from ..pyutils.enum import Enum
from typing import Any

from .definition import (
    GraphQLArgument,
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLField,
    GraphQLInputType,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    is_abstract_type,
    is_enum_type,
    is_input_object_type,
    is_interface_type,
    is_list_type,
    is_named_type,
    is_non_null_type,
    is_object_type,
    is_scalar_type,
    is_union_type,
)
from ..pyutils import is_invalid, OrderedDict
from .scalars import GraphQLBoolean, GraphQLString
from ..language import DirectiveLocation

__all__ = [
    "SchemaMetaFieldDef",
    "TypeKind",
    "TypeMetaFieldDef",
    "TypeNameMetaFieldDef",
    "introspection_types",
    "is_introspection_type",
]


def print_value(value, type_):
    # Since print_value needs graphql.type, it can only be imported later
    from ..utilities.schema_printer import print_value

    return print_value(value, type_)


__Schema = GraphQLObjectType(
    name="__Schema",
    description="A GraphQL Schema defines the capabilities of a GraphQL"
    " server. It exposes all available types and directives"
    " on the server, as well as the entry points for query,"
    " mutation, and subscription operations.",
    fields=lambda: OrderedDict((
        ("types", GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(__Type))),
            resolve=lambda schema, _info: schema.type_map.values(),
            description="A list of all types supported by this server.",
        )),
        ("queryType", GraphQLField(
            GraphQLNonNull(__Type),
            resolve=lambda schema, _info: schema.query_type,
            description="The type that query operations will be rooted at.",
        )),
        ("mutationType", GraphQLField(
            __Type,
            resolve=lambda schema, _info: schema.mutation_type,
            description="If this server supports mutation, the type that"
            " mutation operations will be rooted at.",
        )),
        ("subscriptionType", GraphQLField(
            __Type,
            resolve=lambda schema, _info: schema.subscription_type,
            description="If this server support subscription, the type that"
            " subscription operations will be rooted at.",
        )),
        ("directives", GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(__Directive))),
            resolve=lambda schema, _info: schema.directives,
            description="A list of all directives supported by this server.",
        )),
    )),
)


__Directive = GraphQLObjectType(
    name="__Directive",
    description="A Directive provides a way to describe alternate runtime"
    " execution and type validation behavior in a GraphQL"
    " document.\n\nIn some cases, you need to provide options"
    " to alter GraphQL's execution behavior in ways field"
    " arguments will not suffice, such as conditionally including"
    " or skipping a field. Directives provide this by describing"
    " additional information to the executor.",
    fields=lambda: OrderedDict((
        # Note: The fields onOperation, onFragment and onField are deprecated
        ("name", GraphQLField(
            GraphQLNonNull(GraphQLString), resolve=lambda obj, _info: obj.name
        )),
        ("description", GraphQLField(
            GraphQLString, resolve=lambda obj, _info: obj.description
        )),
        ("locations", GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(__DirectiveLocation))),
            resolve=lambda obj, _info: obj.locations,
        )),
        ("args", GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(__InputValue))),
            resolve=lambda directive, _info: (directive.args or {}).items(),
        )),
    )),
)


__DirectiveLocation = GraphQLEnumType(
    name="__DirectiveLocation",
    description="A Directive can be adjacent to many parts of the GraphQL"
    " language, a __DirectiveLocation describes one such possible"
    " adjacencies.",
    values=OrderedDict((
        ("QUERY", GraphQLEnumValue(
            DirectiveLocation.QUERY,
            description="Location adjacent to a query operation.",
        )),
        ("MUTATION", GraphQLEnumValue(
            DirectiveLocation.MUTATION,
            description="Location adjacent to a mutation operation.",
        )),
        ("SUBSCRIPTION", GraphQLEnumValue(
            DirectiveLocation.SUBSCRIPTION,
            description="Location adjacent to a subscription operation.",
        )),
        ("FIELD", GraphQLEnumValue(
            DirectiveLocation.FIELD, description="Location adjacent to a field."
        )),
        ("FRAGMENT_DEFINITION", GraphQLEnumValue(
            DirectiveLocation.FRAGMENT_DEFINITION,
            description="Location adjacent to a fragment definition.",
        )),
        ("FRAGMENT_SPREAD", GraphQLEnumValue(
            DirectiveLocation.FRAGMENT_SPREAD,
            description="Location adjacent to a fragment spread.",
        )),
        ("INLINE_FRAGMENT", GraphQLEnumValue(
            DirectiveLocation.INLINE_FRAGMENT,
            description="Location adjacent to an inline fragment.",
        )),
        ("VARIABLE_DEFINITION", GraphQLEnumValue(
            DirectiveLocation.VARIABLE_DEFINITION,
            description="Location adjacent to a variable definition.",
        )),
        ("SCHEMA", GraphQLEnumValue(
            DirectiveLocation.SCHEMA,
            description="Location adjacent to a schema definition.",
        )),
        ("SCALAR", GraphQLEnumValue(
            DirectiveLocation.SCALAR,
            description="Location adjacent to a scalar definition.",
        )),
        ("OBJECT", GraphQLEnumValue(
            DirectiveLocation.OBJECT,
            description="Location adjacent to an object type definition.",
        )),
        ("FIELD_DEFINITION", GraphQLEnumValue(
            DirectiveLocation.FIELD_DEFINITION,
            description="Location adjacent to a field definition.",
        )),
        ("ARGUMENT_DEFINITION", GraphQLEnumValue(
            DirectiveLocation.ARGUMENT_DEFINITION,
            description="Location adjacent to an argument definition.",
        )),
        ("INTERFACE", GraphQLEnumValue(
            DirectiveLocation.INTERFACE,
            description="Location adjacent to an interface definition.",
        )),
        ("UNION", GraphQLEnumValue(
            DirectiveLocation.UNION,
            description="Location adjacent to a union definition.",
        )),
        ("ENUM", GraphQLEnumValue(
            DirectiveLocation.ENUM,
            description="Location adjacent to an enum definition.",
        )),
        ("ENUM_VALUE", GraphQLEnumValue(
            DirectiveLocation.ENUM_VALUE,
            description="Location adjacent to an enum value definition.",
        )),
        ("INPUT_OBJECT", GraphQLEnumValue(
            DirectiveLocation.INPUT_OBJECT,
            description="Location adjacent to" " an input object type definition.",
        )),
        ("INPUT_FIELD_DEFINITION", GraphQLEnumValue(
            DirectiveLocation.INPUT_FIELD_DEFINITION,
            description="Location adjacent to" " an input object field definition.",
        )),
    )),
)


__Type = GraphQLObjectType(
    name="__Type",
    description="The fundamental unit of any GraphQL Schema is the type."
    " There are many kinds of types in GraphQL as represented"
    " by the `__TypeKind` enum.\n\nDepending on the kind of a"
    " type, certain fields describe information about that type."
    " Scalar types provide no information beyond a name and"
    " description, while Enum types provide their values."
    " Object and Interface types provide the fields they describe."
    " Abstract types, Union and Interface, provide the Object"
    " types possible at runtime. List and NonNull types compose"
    " other types.",
    fields=lambda: OrderedDict((
        ("kind", GraphQLField(
            GraphQLNonNull(__TypeKind), resolve=TypeFieldResolvers.kind
        )),
        ("name", GraphQLField(GraphQLString, resolve=TypeFieldResolvers.name)),
        ("description", GraphQLField(
            GraphQLString, resolve=TypeFieldResolvers.description
        )),
        ("fields", GraphQLField(
            GraphQLList(GraphQLNonNull(__Field)),
            args=OrderedDict((
                ("includeDeprecated", GraphQLArgument(
                    GraphQLBoolean, default_value=False
                )),
            )),
            resolve=TypeFieldResolvers.fields,
        )),
        ("interfaces", GraphQLField(
            GraphQLList(GraphQLNonNull(__Type)), resolve=TypeFieldResolvers.interfaces
        )),
        ("possibleTypes", GraphQLField(
            GraphQLList(GraphQLNonNull(__Type)),
            resolve=TypeFieldResolvers.possible_types,
        )),
        ("enumValues", GraphQLField(
            GraphQLList(GraphQLNonNull(__EnumValue)),
            args=OrderedDict((
                ("includeDeprecated", GraphQLArgument(
                    GraphQLBoolean, default_value=False
                )),
            )),
            resolve=TypeFieldResolvers.enum_values,
        )),
        ("inputFields", GraphQLField(
            GraphQLList(GraphQLNonNull(__InputValue)),
            resolve=TypeFieldResolvers.input_fields,
        )),
        ("ofType", GraphQLField(__Type, resolve=TypeFieldResolvers.of_type)),
    )),
)


class TypeFieldResolvers(object):
    @staticmethod
    def kind(type_, _info):
        if is_scalar_type(type_):
            return TypeKind.SCALAR
        if is_object_type(type_):
            return TypeKind.OBJECT
        if is_interface_type(type_):
            return TypeKind.INTERFACE
        if is_union_type(type_):
            return TypeKind.UNION
        if is_enum_type(type_):
            return TypeKind.ENUM
        if is_input_object_type(type_):
            return TypeKind.INPUT_OBJECT
        if is_list_type(type_):
            return TypeKind.LIST
        if is_non_null_type(type_):
            return TypeKind.NON_NULL
        raise TypeError("Unknown kind of type: {}".format(type_))

    @staticmethod
    def name(type_, _info):
        return getattr(type_, "name", None)

    @staticmethod
    def description(type_, _info):
        return getattr(type_, "description", None)

    # noinspection PyPep8Naming
    @staticmethod
    def fields(type_, _info, includeDeprecated=False):
        if is_object_type(type_) or is_interface_type(type_):
            items = type_.fields.items()
            if not includeDeprecated:
                return [item for item in items if not item[1].deprecation_reason]
            return list(items)

    @staticmethod
    def interfaces(type_, _info):
        if is_object_type(type_):
            return type_.interfaces

    @staticmethod
    def possible_types(type_, info):
        if is_abstract_type(type_):
            return info.schema.get_possible_types(type_)

    # noinspection PyPep8Naming
    @staticmethod
    def enum_values(type_, _info, includeDeprecated=False):
        if is_enum_type(type_):
            items = type_.values.items()
            if not includeDeprecated:
                return [item for item in items if not item[1].deprecation_reason]
            return items

    @staticmethod
    def input_fields(type_, _info):
        if is_input_object_type(type_):
            return type_.fields.items()

    @staticmethod
    def of_type(type_, _info):
        return getattr(type_, "of_type", None)


__Field = GraphQLObjectType(
    name="__Field",
    description="Object and Interface types are described by a list of Fields,"
    " each of which has a name, potentially a list of arguments,"
    " and a return type.",
    fields=lambda: OrderedDict((
        ("name", GraphQLField(
            GraphQLNonNull(GraphQLString), resolve=lambda item, _info: item[0]
        )),
        ("description", GraphQLField(
            GraphQLString, resolve=lambda item, _info: item[1].description
        )),
        ("args", GraphQLField(
            GraphQLNonNull(GraphQLList(GraphQLNonNull(__InputValue))),
            resolve=lambda item, _info: (item[1].args or {}).items(),
        )),
        ("type", GraphQLField(
            GraphQLNonNull(__Type), resolve=lambda item, _info: item[1].type
        )),
        ("isDeprecated", GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            resolve=lambda item, _info: item[1].is_deprecated,
        )),
        ("deprecationReason", GraphQLField(
            GraphQLString, resolve=lambda item, _info: item[1].deprecation_reason
        )),
    )),
)


__InputValue = GraphQLObjectType(
    name="__InputValue",
    description="Arguments provided to Fields or Directives and the input"
    " fields of an InputObject are represented as Input Values"
    " which describe their type and optionally a default value.",
    fields=lambda: OrderedDict((
        ("name", GraphQLField(
            GraphQLNonNull(GraphQLString), resolve=lambda item, _info: item[0]
        )),
        ("description", GraphQLField(
            GraphQLString, resolve=lambda item, _info: item[1].description
        )),
        ("type", GraphQLField(
            GraphQLNonNull(__Type), resolve=lambda item, _info: item[1].type
        )),
        ("defaultValue", GraphQLField(
            GraphQLString,
            description="A GraphQL-formatted string representing"
            " the default value for this input value.",
            resolve=lambda item, _info: None
            if is_invalid(item[1].default_value)
            else print_value(item[1].default_value, item[1].type),
        )),
    )),
)


__EnumValue = GraphQLObjectType(
    name="__EnumValue",
    description="One possible value for a given Enum. Enum values are unique"
    " values, not a placeholder for a string or numeric value."
    " However an Enum value is returned in a JSON response as a"
    " string.",
    fields=lambda: OrderedDict((
        ("name", GraphQLField(
            GraphQLNonNull(GraphQLString), resolve=lambda item, _info: item[0]
        )),
        ("description", GraphQLField(
            GraphQLString, resolve=lambda item, _info: item[1].description
        )),
        ("isDeprecated", GraphQLField(
            GraphQLNonNull(GraphQLBoolean),
            resolve=lambda item, _info: item[1].is_deprecated,
        )),
        ("deprecationReason", GraphQLField(
            GraphQLString, resolve=lambda item, _info: item[1].deprecation_reason
        )),
    )),
)


class TypeKind(Enum):
    SCALAR = "scalar"
    OBJECT = "object"
    INTERFACE = "interface"
    UNION = "union"
    ENUM = "enum"
    INPUT_OBJECT = "input object"
    LIST = "list"
    NON_NULL = "non-null"


__TypeKind = GraphQLEnumType(
    name="__TypeKind",
    description="An enum describing what kind of type a given `__Type` is.",
    values=OrderedDict((
        ("SCALAR", GraphQLEnumValue(
            TypeKind.SCALAR, description="Indicates this type is a scalar."
        )),
        ("OBJECT", GraphQLEnumValue(
            TypeKind.OBJECT,
            description="Indicates this type is an object. "
            "`fields` and `interfaces` are valid fields.",
        )),
        ("INTERFACE", GraphQLEnumValue(
            TypeKind.INTERFACE,
            description="Indicates this type is an interface. "
            "`fields` and `possibleTypes` are valid fields.",
        )),
        ("UNION", GraphQLEnumValue(
            TypeKind.UNION,
            description="Indicates this type is a union. "
            "`possibleTypes` is a valid field.",
        )),
        ("ENUM", GraphQLEnumValue(
            TypeKind.ENUM,
            description="Indicates this type is an enum. "
            "`enumValues` is a valid field.",
        )),
        ("INPUT_OBJECT", GraphQLEnumValue(
            TypeKind.INPUT_OBJECT,
            description="Indicates this type is an input object. "
            "`inputFields` is a valid field.",
        )),
        ("LIST", GraphQLEnumValue(
            TypeKind.LIST,
            description="Indicates this type is a list. " "`ofType` is a valid field.",
        )),
        ("NON_NULL", GraphQLEnumValue(
            TypeKind.NON_NULL,
            description="Indicates this type is a non-null. "
            "`ofType` is a valid field.",
        )),
    )),
)


SchemaMetaFieldDef = GraphQLField(
    GraphQLNonNull(__Schema),  # name = '__schema'
    description="Access the current type schema of this server.",
    args=OrderedDict(),
    resolve=lambda source, info: info.schema,
)


TypeMetaFieldDef = GraphQLField(
    __Type,  # name = '__type'
    description="Request the type information of a single type.",
    args=OrderedDict((
        ("name", GraphQLArgument(GraphQLNonNull(GraphQLString)),
    ),)),
    resolve=lambda source, info, **args: info.schema.get_type(args["name"]),
)


TypeNameMetaFieldDef = GraphQLField(
    GraphQLNonNull(GraphQLString),  # name='__typename'
    description="The name of the current Object type at runtime.",
    args=OrderedDict(),
    resolve=lambda source, info, **args: info.parent_type.name,
)


# Since double underscore names are subject to name mangling in Python,
# the introspection classes are best imported via this dictionary:
introspection_types = OrderedDict((
    ("__Schema", __Schema),
    ("__Directive", __Directive),
    ("__DirectiveLocation", __DirectiveLocation),
    ("__Type", __Type),
    ("__Field", __Field),
    ("__InputValue", __InputValue),
    ("__EnumValue", __EnumValue),
    ("__TypeKind", __TypeKind),
))


def is_introspection_type(type_):
    return is_named_type(type_) and type_.name in introspection_types
