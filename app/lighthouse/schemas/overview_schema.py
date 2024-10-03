from marshmallow import Schema, fields

class OverviewSchema(Schema):
    performance = fields.Float(required=True)
    accessibility = fields.Float(required=True)
    best_practices = fields.Float(required=True)
    seo = fields.Float(required=True)
