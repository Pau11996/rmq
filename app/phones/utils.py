from sqlalchemy import func, select, cast, BigInteger, case
from sqlalchemy.orm import Session
from app.phones.models import PhoneData
from app.phones.phone_schema import DurationCounts, PhoneDataSchema
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.sql.expression import Executable
from sqlalchemy.ext.compiler import compiles


class Explain(Executable, ClauseElement):
    def __init__(self, stmt, analyze=False):
        self.statement = stmt
        self.analyze = analyze


@compiles(Explain, "postgresql")
def pg_explain(element, compiler, **kw):
    text = "EXPLAIN "
    if element.analyze:
        text += "ANALYZE "
    text += compiler.process(element.statement, **kw)

    return text


async def generate_report(session: Session, phone: str) -> PhoneDataSchema | None:
    query = select(
        PhoneData.phone,
        func.count().label('cnt_all_attempts'),
        func.count(
            case((PhoneData.end_date - PhoneData.start_date < 10000, 1), else_=None)
        ).label('cnt_att_dur_10_sec'),
        func.count(
            case(((PhoneData.end_date - PhoneData.start_date >= 10000) & (
                    PhoneData.end_date - PhoneData.start_date < 30000), 1), else_=None)
        ).label('cnt_att_dur_10_30_sec'),
        func.count(
            case((PhoneData.end_date - PhoneData.start_date >= 30000, 1), else_=None)
        ).label('cnt_att_dur_30_sec'),
        func.min(cast((PhoneData.end_date - PhoneData.start_date) * 10, BigInteger)).label(
            'min_price_att'),
        func.max(cast((PhoneData.end_date - PhoneData.start_date) * 10, BigInteger)).label(
            'max_price_att'),
        func.avg(PhoneData.end_date - PhoneData.start_date).label('avg_dur_att'),
        func.sum(
            case(((PhoneData.end_date - PhoneData.start_date) > 15000,
                  cast((PhoneData.end_date - PhoneData.start_date) * 10, BigInteger))), else_=0
        ).label('sum_price_att_over_15')
    ).where(PhoneData.phone == phone).group_by(PhoneData.phone)

    result_phone = session.execute(query)
    result_phone = result_phone.fetchone()

    if result_phone:
        phone_data = PhoneDataSchema(
            phone=result_phone.phone,
            cnt_all_attempts=result_phone.cnt_all_attempts,
            cnt_att_dur=DurationCounts(
                sec_10=result_phone.cnt_att_dur_10_sec,
                sec_10_30=result_phone.cnt_att_dur_10_30_sec,
                sec_30=result_phone.cnt_att_dur_30_sec
            ),
            min_price_att=result_phone.min_price_att,
            max_price_att=result_phone.max_price_att,
            avg_dur_att=result_phone.avg_dur_att,
            sum_price_att_over_15=result_phone.sum_price_att_over_15
        )
        return phone_data
    else:
        return None
