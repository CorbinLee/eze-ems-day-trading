# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: market_data.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
import utilities_pb2 as utilities__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11market_data.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x0futilities.proto\"T\n\x0bOptionTypes\x12\'\n\tCallOrPut\x18\x01 \x01(\x0e\x32\x14.OptionTypes.Options\"\x1c\n\x07Options\x12\x08\n\x04\x43\x41LL\x10\x00\x12\x07\n\x03PUT\x10\x01\"g\n\x08Interval\x12,\n\x11\x42\x61rIntervalOption\x18\x01 \x01(\x0e\x32\x11.Interval.Options\"-\n\x07Options\x12\t\n\x05\x44\x41ILY\x10\x00\x12\n\n\x06WEEKLY\x10\x01\x12\x0b\n\x07MONTHLY\x10\x02\"\xbf\x01\n\tTickTypes\x12$\n\nTickOption\x18\x01 \x01(\x0e\x32\x10.TickTypes.Ticks\"\x8b\x01\n\x05Ticks\x12\t\n\x05TRADE\x10\x00\x12\x07\n\x03\x42ID\x10\x01\x12\x07\n\x03\x41SK\x10\x02\x12\x10\n\x0cREGIONAL_BID\x10\x03\x12\x10\n\x0cREGIONAL_ASK\x10\x04\x12\x0b\n\x07\x44\x45LETED\x10\x0b\x12\x0c\n\x08INSERTED\x10\x0c\x12\x14\n\x10IRREGULAR_DELETE\x10,\x12\x10\n\x0c\x46ORM_T_TRADE\x10 \"\xbc\x01\n\x10\x43ommonBarsFields\x12\x0e\n\x06\x41\x63Vol1\x18\x02 \x03(\x05\x12\r\n\x05\x43ount\x18\x03 \x01(\x05\x12\x15\n\x05High1\x18\x04 \x03(\x0b\x32\x06.Price\x12\x14\n\x04Low1\x18\x05 \x03(\x0b\x32\x06.Price\x12\x17\n\x07OpenPrc\x18\x06 \x03(\x0b\x32\x06.Price\x12\x16\n\x06Settle\x18\x07 \x03(\x0b\x32\x06.Price\x12+\n\x07TrdDate\x18\x08 \x03(\x0b\x32\x1a.google.protobuf.Timestamp\"\x8c\x02\n\x1d\x44\x61ilyWeeklyMonthlyBarsRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0e\n\x06Symbol\x18\x02 \x01(\t\x12\x1a\n\x07Interim\x18\x03 \x01(\x0b\x32\t.Interval\x12,\n\x08StopDate\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\x08\x44\x61ysBack\x18\x05 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12.\n\tRequestId\x18\x06 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x0f\n\x07Request\x18\x07 \x01(\x08\x12\x0e\n\x06\x41\x64vise\x18\x08 \x01(\x08\"\x89\x01\n\x1e\x44\x61ilyWeeklyMonthlyBarsResponse\x12$\n\tBarFields\x18\x01 \x01(\x0b\x32\x11.CommonBarsFields\x12\x10\n\x08\x44ispName\x18\x02 \x01(\t\x12/\n\x0f\x41\x63knowledgement\x18\x03 \x01(\x0b\x32\x16.ServerAcknowledgement\"\xce\x02\n\x13IntradayBarsRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0e\n\x06Symbol\x18\x02 \x01(\t\x12\x13\n\x0b\x42\x61rInterval\x18\x03 \x01(\x05\x12\x10\n\x08\x44\x61ysBack\x18\x04 \x01(\x05\x12\x17\n\x0fStartAtMidnight\x18\x05 \x01(\x08\x12(\n\x04\x44\x61te\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\tStartTime\x18\x07 \x01(\x0b\x32\x19.google.protobuf.Duration\x12+\n\x08StopTime\x18\x08 \x01(\x0b\x32\x19.google.protobuf.Duration\x12.\n\trequestId\x18\t \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x0f\n\x07Request\x18\n \x01(\x08\x12\x0e\n\x06\x41\x64vise\x18\x0b \x01(\x08\"y\n\x14IntradayBarsResponse\x12\x1f\n\x04\x42\x61rs\x18\x01 \x01(\x0b\x32\x11.CommonBarsFields\x12\x0f\n\x07TrdTim1\x18\x02 \x03(\t\x12/\n\x0f\x41\x63knowledgement\x18\x03 \x01(\x0b\x32\x16.ServerAcknowledgement\"\x90\x01\n\"OptionSymbolFromDescriptionRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0c\n\x04Root\x18\x02 \x01(\t\x12\x12\n\nExpiration\x18\x03 \x01(\t\x12 \n\nOptionType\x18\x04 \x01(\x0b\x32\x0c.OptionTypes\x12\x13\n\x0bStrikePrice\x18\x05 \x01(\x01\"f\n#OptionSymbolFromDescriptionResponse\x12\x0e\n\x06Symbol\x18\x01 \x01(\t\x12/\n\x0f\x41\x63knowledgement\x18\x02 \x01(\x0b\x32\x16.ServerAcknowledgement\"G\n\"DescriptionFromOptionSymbolRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0e\n\x06Symbol\x18\x02 \x01(\t\"\xaf\x01\n#DescriptionFromOptionSymbolResponse\x12\x0c\n\x04Root\x18\x01 \x01(\t\x12\x12\n\nExpiration\x18\x02 \x01(\t\x12 \n\nOptionType\x18\x03 \x01(\x0b\x32\x0c.OptionTypes\x12\x13\n\x0bStrikePrice\x18\x04 \x01(\x01\x12/\n\x0f\x41\x63knowledgement\x18\x05 \x01(\x0b\x32\x16.ServerAcknowledgement\"{\n\x17Level1MarketDataRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0f\n\x07Symbols\x18\x02 \x03(\t\x12\x1b\n\x13RegionalExchangeIds\x18\x03 \x03(\t\x12\x0f\n\x07Request\x18\x04 \x01(\x08\x12\x0e\n\x06\x41\x64vise\x18\x05 \x01(\x08\"\xa7\x06\n\x18Level1MarketDataResponse\x12/\n\x0f\x41\x63knowledgement\x18\x01 \x01(\x0b\x32\x16.ServerAcknowledgement\x12\x10\n\x08\x44ispName\x18\x02 \x01(\t\x12\x17\n\x07Trdprc1\x18\x03 \x01(\x0b\x32\x06.Price\x12*\n\x07Trdtim1\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x12\n\nSymbolDesc\x18\x05 \x01(\t\x12\x13\n\x0b\x43ompanyName\x18\x06 \x01(\t\x12\x38\n\x13\x41rcaImbalanceVolume\x18\x08 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x34\n\x0f\x41rcaMatchVolume\x18\t \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x38\n\x13SaleConditionVolume\x18\n \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x36\n\x11IntradayHighCount\x18\x0b \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12,\n\x07VwapVol\x18\x0c \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12*\n\x04Vwap\x18\r \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x13\n\x03\x42id\x18\x0f \x01(\x0b\x32\x06.Price\x12\x13\n\x03\x41sk\x18\x11 \x01(\x0b\x32\x06.Price\x12\x1a\n\nChangeLast\x18\x12 \x01(\x0b\x32\x06.Price\x12\x15\n\x05High1\x18\x13 \x01(\x0b\x32\x06.Price\x12\x16\n\x06High52\x18\x14 \x01(\x0b\x32\x06.Price\x12\x14\n\x04Low1\x18\x15 \x01(\x0b\x32\x06.Price\x12\x15\n\x05Low52\x18\x16 \x01(\x0b\x32\x06.Price\x12\x45\n\x0e\x45xtendedFields\x18\x17 \x03(\x0b\x32-.Level1MarketDataResponse.ExtendedFieldsEntry\x1a\x35\n\x13\x45xtendedFieldsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"1\n\x1cUnSubscribeLevel1DataRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\"\xba\x01\n\x1dUnSubscribeLevel1DataResponse\x12\x16\n\x0eServerResponse\x18\x01 \x01(\t\x12J\n\x0eOptionalFields\x18\x02 \x03(\x0b\x32\x32.UnSubscribeLevel1DataResponse.OptionalFieldsEntry\x1a\x35\n\x13OptionalFieldsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"P\n\x11\x41\x64\x64SymbolsRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0f\n\x07Symbols\x18\x02 \x03(\t\x12\x17\n\x0fMarketDataLevel\x18\x03 \x01(\t\"\xa4\x01\n\x12\x41\x64\x64SymbolsResponse\x12\x16\n\x0eServerResponse\x18\x01 \x01(\t\x12?\n\x0eOptionalFields\x18\x02 \x03(\x0b\x32\'.AddSymbolsResponse.OptionalFieldsEntry\x1a\x35\n\x13OptionalFieldsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"S\n\x14RemoveSymbolsRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0f\n\x07Symbols\x18\x02 \x03(\t\x12\x17\n\x0fMarketDataLevel\x18\x03 \x01(\t\"\xaa\x01\n\x15RemoveSymbolsResponse\x12\x16\n\x0eServerResponse\x18\x01 \x01(\t\x12\x42\n\x0eOptionalFields\x18\x02 \x03(\x0b\x32*.RemoveSymbolsResponse.OptionalFieldsEntry\x1a\x35\n\x13OptionalFieldsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xa4\x01\n\x17Level2MarketDataRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0f\n\x07Symbols\x18\x02 \x03(\t\x12.\n\tRequestId\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x14\n\x0cMarketSource\x18\x04 \x03(\t\x12\x0f\n\x07Request\x18\x05 \x01(\x08\x12\x0e\n\x06\x41\x64vise\x18\x06 \x01(\x08\"\x88\x06\n\x18Level2MarketDataResponse\x12/\n\x0f\x41\x63knowledgement\x18\x01 \x01(\x0b\x32\x16.ServerAcknowledgement\x12\x11\n\tMktSource\x18\x02 \x01(\t\x12\x10\n\x08MktMkrId\x18\x03 \x01(\t\x12\x10\n\x08\x44ispName\x18\x04 \x01(\t\x12\x14\n\x0cMktMkrStatus\x18\x05 \x01(\t\x12\x10\n\x08\x45xchName\x18\x06 \x01(\t\x12\x15\n\rMktMkrDisplay\x18\x07 \x01(\t\x12\x32\n\rMktMkrBidsize\x18\x08 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x32\n\rMktMkrAsksize\x18\t \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12-\n\x08SymbolId\x18\n \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x30\n\x0bSymbolError\x18\x0b \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12,\n\x07TableId\x18\x0c \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12)\n\x04Styp\x18\r \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x34\n\x0fQuoteUpdateType\x18\x0e \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12.\n\nMktMkrDate\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\rMktMkrBidTime\x18\x10 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x30\n\rMktMkrAskTime\x18\x11 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x19\n\tMktMkrBid\x18\x12 \x01(\x0b\x32\x06.Price\x12#\n\x13MktMkrChangeLastAsk\x18\x13 \x01(\x0b\x32\x06.Price\x12\x19\n\tMktMkrAsk\x18\x14 \x01(\x0b\x32\x06.Price\"1\n\x1cUnSubscribeLevel2DataRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\"\xba\x01\n\x1dUnSubscribeLevel2DataResponse\x12\x16\n\x0eServerResponse\x18\x01 \x01(\t\x12J\n\x0eOptionalFields\x18\x02 \x03(\x0b\x32\x32.UnSubscribeLevel2DataResponse.OptionalFieldsEntry\x1a\x35\n\x13OptionalFieldsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"k\n\x12OptionChainRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x12\n\nSymbolRoot\x18\x02 \x01(\t\x12.\n\tRequestId\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\"\xae\x02\n\x12QuoteChainResponse\x12\x10\n\x08\x44ispName\x18\x02 \x01(\t\x12\x10\n\x08\x45xchName\x18\x03 \x01(\t\x12\x12\n\nSymbolDesc\x18\x04 \x01(\t\x12\x10\n\x08TrdUnits\x18\x05 \x01(\t\x12\x15\n\rCommodityName\x18\x06 \x01(\t\x12)\n\x04Styp\x18\x07 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12,\n\x07Session\x18\x08 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12,\n\x07Minmove\x18\t \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x30\n\nBasisvalue\x18\n \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\"o\n\x13OptionChainResponse\x12/\n\x0f\x41\x63knowledgement\x18\x01 \x01(\x0b\x32\x16.ServerAcknowledgement\x12\'\n\nDerivative\x18\x02 \x03(\x0b\x32\x13.QuoteChainResponse\"?\n\x1aSymbolReferenceDataRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0e\n\x06Symbol\x18\x02 \x01(\t\"\xc6\x01\n\x0fSymInfoResponse\x12)\n\x04Styp\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x10\n\x08\x44ispName\x18\x02 \x01(\t\x12\x15\n\rBloombergCode\x18\x03 \x01(\t\x12\x19\n\x11\x42loombergCodeFull\x18\x04 \x01(\t\x12\x1e\n\x16\x42loombergCodeComposite\x18\x05 \x01(\t\x12\x10\n\x08\x45xchName\x18\x06 \x01(\t\x12\x12\n\nSymbolDesc\x18\x07 \x01(\t\"u\n\x1bSymbolReferenceDataResponse\x12/\n\x0f\x41\x63knowledgement\x18\x01 \x01(\x0b\x32\x16.ServerAcknowledgement\x12%\n\x0bSymInfoList\x18\x02 \x03(\x0b\x32\x10.SymInfoResponse\"\xa9\x02\n\x0fTickDataRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0e\n\x06Symbol\x18\x02 \x01(\t\x12(\n\x04\x44\x61te\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\tStartTime\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12+\n\x08StopTime\x18\x05 \x01(\x0b\x32\x19.google.protobuf.Duration\x12.\n\tRequestId\x18\x06 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x1d\n\tTickTypes\x18\x07 \x03(\x0b\x32\n.TickTypes\x12\x0f\n\x07Request\x18\x08 \x01(\x08\x12\x0e\n\x06\x41\x64vise\x18\t \x01(\x08\"\xd6\x01\n\rTicksResponse\x12\x17\n\x07TrdPrc1\x18\x02 \x03(\x0b\x32\x06.Price\x12+\n\x07TrdDate\x18\x03 \x03(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08TickType\x18\x04 \x03(\x05\x12\x0f\n\x07TrdXid1\x18\x05 \x03(\t\x12\x0f\n\x07TrdVol1\x18\x06 \x03(\x05\x12*\n\x07TrdTim1\x18\x07 \x03(\x0b\x32\x19.google.protobuf.Duration\x12\x10\n\x08\x44ispName\x18\x08 \x03(\t\x12\r\n\x05\x43ount\x18\t \x01(\x05\"e\n\x10TickDataResponse\x12/\n\x0f\x41\x63knowledgement\x18\x01 \x01(\x0b\x32\x16.ServerAcknowledgement\x12 \n\x08TickInfo\x18\x02 \x03(\x0b\x32\x0e.TicksResponse\"a\n\x1aOptionsAndGreekDataRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0f\n\x07Symbols\x18\x02 \x03(\t\x12\x0f\n\x07Request\x18\x03 \x01(\x08\x12\x0e\n\x06\x41\x64vise\x18\x04 \x01(\x08\"\xd8\t\n\x19OptionCalculationResponse\x12*\n\x05Model\x18\x01 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12+\n\x05Theta\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12+\n\x05Gamma\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12*\n\x04Vega\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12+\n\x05\x44\x65lta\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12-\n\x07Premium\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x30\n\nImpliedVol\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x34\n\x0e\x44ividendAmout6\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x34\n\x0e\x44ividendAmout5\x18\t \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x34\n\x0e\x44ividendAmout4\x18\n \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x34\n\x0e\x44ividendAmout3\x18\x0b \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x34\n\x0e\x44ividendAmout2\x18\x0c \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x34\n\x0e\x44ividendAmout1\x18\r \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12*\n\x04Rate\x18\x0e \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x32\n\x0cTimeToExpire\x18\x0f \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x1e\n\x0eUnderlierPrice\x18\x10 \x01(\x0b\x32\x06.Price\x12\x1d\n\rOriginalPrice\x18\x11 \x01(\x0b\x32\x06.Price\x12\x1b\n\x0bStrikePrice\x18\x12 \x01(\x0b\x32\x06.Price\x12\x31\n\rDividendDate6\x18\x13 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rDividendDate5\x18\x14 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rDividendDate4\x18\x15 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rDividendDate3\x18\x16 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rDividendDate2\x18\x17 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rDividendDate1\x18\x18 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x11\n\tPutCallId\x18\x19 \x01(\t\x12\x10\n\x08\x44ispName\x18\x1a \x01(\t\x12\x10\n\x08UnderSym\x18\x1b \x01(\t\x12\x12\n\nOptionRoot\x18\x1c \x01(\t\"\x7f\n\x1bOptionsAndGreekDataResponse\x12/\n\x0f\x41\x63knowledgement\x18\x01 \x01(\x0b\x32\x16.ServerAcknowledgement\x12/\n\x0bOptionsList\x18\x02 \x03(\x0b\x32\x1a.OptionCalculationResponse\"8\n\x13SecurityDataRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0e\n\x06Symbol\x18\x02 \x01(\t\"\xef\x10\n\x0cSecurityData\x12.\n\nDivpaydate\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\tExdivdate\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nHigh52Date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\tLow52Date\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08ProcDate\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nSplitDate1\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\x08\x41\x64x14d1d\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x39\n\x13\x42ollingerLower21d1d\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x39\n\x13\x42ollingerUpper21d1d\x18\t \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x33\n\rClose10davg1d\x18\n \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x34\n\x0e\x43lose200davg1d\x18\x0b \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x33\n\rClose20davg1d\x18\x0c \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x33\n\rClose50davg1d\x18\r \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x32\n\x0c\x43lose5davg1d\x18\x0e \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x32\n\x0cHigh15dmax1d\x18\x0f \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x37\n\x11Hlvolatility10d1d\x18\x10 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x31\n\x0bLow15dmin1d\x18\x11 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x32\n\x0cMinusdi14d1d\x18\x12 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x31\n\x0bPlusdi14d1d\x18\x13 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12.\n\x08Rsi14d1d\x18\x14 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12.\n\x08Rsi25d1d\x18\x15 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12-\n\x07Rsi9d1d\x18\x16 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x32\n\x0cSplitFactor1\x18\x17 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x34\n\x0eVolume10davg1d\x18\x18 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x35\n\x0fVolume200davg1d\x18\x19 \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x34\n\x0eVolume20davg1d\x18\x1a \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x34\n\x0eVolume50davg1d\x18\x1b \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x33\n\rVolume5davg1d\x18\x1c \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x32\n\rDividendFreqN\x18\x1d \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x35\n\x10SecurityCategory\x18\x1e \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12.\n\tSharesOut\x18\x1f \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x14\n\x04\x42\x65ta\x18  \x01(\x0b\x32\x06.Price\x12\x18\n\x08\x44ividend\x18! \x01(\x0b\x32\x06.Price\x12\x1c\n\x0c\x44ividendRate\x18\" \x01(\x0b\x32\x06.Price\x12\x1d\n\rDividendYield\x18# \x01(\x0b\x32\x06.Price\x12\x18\n\x08\x45\x61rnings\x18$ \x01(\x0b\x32\x06.Price\x12\x16\n\x06High52\x18% \x01(\x0b\x32\x06.Price\x12\x15\n\x05Low52\x18& \x01(\x0b\x32\x06.Price\x12\x16\n\x06MgSicm\x18\' \x01(\x0b\x32\x06.Price\x12\x16\n\x06MktCap\x18( \x01(\x0b\x32\x06.Price\x12\x17\n\x07Peratio\x18) \x01(\x0b\x32\x06.Price\x12\x15\n\rBloombergCode\x18* \x01(\t\x12\x1e\n\x16\x42loombergCodeComposite\x18+ \x01(\t\x12\x13\n\x0b\x43ompanyName\x18, \x01(\t\x12\x0f\n\x07\x43ountry\x18- \x01(\t\x12\r\n\x05\x43usip\x18. \x01(\t\x12\x10\n\x08\x44ispName\x18/ \x01(\t\x12\x14\n\x0cGicsIndustry\x18\x30 \x01(\t\x12\x12\n\nGicsSector\x18\x31 \x01(\t\x12\x17\n\x0fGicsSubindustry\x18\x32 \x01(\t\x12\x0e\n\x06IsinNo\x18\x33 \x01(\t\x12\x18\n\x10IssuersSectorStr\x18\x34 \x01(\t\x12\x17\n\x0fPrimaryExchange\x18\x35 \x01(\t\x12\x0f\n\x07RicCode\x18\x36 \x01(\t\x12\r\n\x05Sedol\x18\x37 \x01(\t\"p\n\x14SecurityDataResponse\x12/\n\x0f\x41\x63knowledgement\x18\x01 \x01(\x0b\x32\x16.ServerAcknowledgement\x12\'\n\x10SecurityInfoList\x18\x02 \x03(\x0b\x32\r.SecurityData\"\xeb\x02\n\nSymbolData\x12\x10\n\x08\x44ispName\x18\x01 \x01(\t\x12\x10\n\x08\x45xchName\x18\x02 \x01(\t\x12)\n\x04Styp\x18\x03 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x12\n\nSymbolDesc\x18\x04 \x01(\t\x12\x0e\n\x06IsinNo\x18\x05 \x01(\t\x12\x0f\n\x07\x43ountry\x18\x06 \x01(\t\x12\x15\n\rCommodityName\x18\x07 \x01(\t\x12\x15\n\rBloombergCode\x18\x08 \x01(\t\x12\x19\n\x11\x42loombergCodeFull\x18\t \x01(\t\x12\x1e\n\x16\x42loombergCodeComposite\x18\n \x01(\t\x12\x0f\n\x07RicCode\x18\x0b \x01(\t\x12\r\n\x05Sedol\x18\x0c \x01(\t\x12\x12\n\nGicsSector\x18\r \x01(\t\x12\x14\n\x0cGicsIndustry\x18\x0e \x01(\t\x12\x17\n\x0fGicsSubindustry\x18\x0f \x01(\t\x12\r\n\x05\x43usip\x18\x10 \x01(\t\"G\n\x1dSymbolsFromCompanyNameRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x13\n\x0b\x43ompanyName\x18\x02 \x01(\t\"v\n\x1eSymbolsFromCompanyNameResponse\x12/\n\x0f\x41\x63knowledgement\x18\x01 \x01(\x0b\x32\x16.ServerAcknowledgement\x12#\n\x0eSymbolDatalist\x18\x02 \x03(\x0b\x32\x0b.SymbolData\"\x88\x01\n\x12\x41lternateSymbology\x12\x33\n\x0cSymbolOption\x18\x01 \x01(\x0e\x32\x1d.AlternateSymbology.Symbology\"=\n\tSymbology\x12\x08\n\x04ISIN\x10\x00\x12\t\n\x05SEDOL\x10\x01\x12\x07\n\x03RIC\x10\x02\x12\t\n\x05\x43USIP\x10\x03\x12\x07\n\x03\x42\x42G\x10\x04\"q\n#SymbolFromAlternateSymbologyRequest\x12\x11\n\tUserToken\x18\x01 \x01(\t\x12\x0e\n\x06Symbol\x18\x02 \x01(\t\x12\'\n\nSymbolInfo\x18\x03 \x01(\x0b\x32\x13.AlternateSymbology\"|\n$SymbolFromAlternateSymbologyResponse\x12/\n\x0f\x41\x63knowledgement\x18\x01 \x01(\x0b\x32\x16.ServerAcknowledgement\x12#\n\x0eSymbolInfolist\x18\x02 \x03(\x0b\x32\x0b.SymbolData\"\xf2\x05\n\x16Level1MarketDataRecord\x12\x10\n\x08\x44ispName\x18\x02 \x01(\t\x12\x17\n\x07Trdprc1\x18\x03 \x01(\x0b\x32\x06.Price\x12*\n\x07Trdtim1\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12\x12\n\nSymbolDesc\x18\x05 \x01(\t\x12\x13\n\x0b\x43ompanyName\x18\x06 \x01(\t\x12\x38\n\x13\x41rcaImbalanceVolume\x18\x08 \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x34\n\x0f\x41rcaMatchVolume\x18\t \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x38\n\x13SaleConditionVolume\x18\n \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12\x36\n\x11IntradayHighCount\x18\x0b \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12,\n\x07VwapVol\x18\x0c \x01(\x0b\x32\x1b.google.protobuf.Int32Value\x12*\n\x04Vwap\x18\r \x01(\x0b\x32\x1c.google.protobuf.DoubleValue\x12\x13\n\x03\x42id\x18\x0f \x01(\x0b\x32\x06.Price\x12\x13\n\x03\x41sk\x18\x11 \x01(\x0b\x32\x06.Price\x12\x1a\n\nChangeLast\x18\x12 \x01(\x0b\x32\x06.Price\x12\x15\n\x05High1\x18\x13 \x01(\x0b\x32\x06.Price\x12\x16\n\x06High52\x18\x14 \x01(\x0b\x32\x06.Price\x12\x14\n\x04Low1\x18\x15 \x01(\x0b\x32\x06.Price\x12\x15\n\x05Low52\x18\x16 \x01(\x0b\x32\x06.Price\x12\x43\n\x0e\x45xtendedFields\x18\x17 \x03(\x0b\x32+.Level1MarketDataRecord.ExtendedFieldsEntry\x1a\x35\n\x13\x45xtendedFieldsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"~\n\x1eLevel1MarketDataRecordResponse\x12/\n\x0f\x41\x63knowledgement\x18\x01 \x01(\x0b\x32\x16.ServerAcknowledgement\x12+\n\nDataRecord\x18\x02 \x03(\x0b\x32\x17.Level1MarketDataRecord2\xd7\x0b\n\x11MarketDataService\x12\\\n\x19GetDailyWeeklyMonthlyBars\x12\x1e.DailyWeeklyMonthlyBarsRequest\x1a\x1f.DailyWeeklyMonthlyBarsResponse\x12>\n\x0fGetIntradayBars\x12\x14.IntradayBarsRequest\x1a\x15.IntradayBarsResponse\x12G\n\x1aGetOptionChainForUnderlier\x12\x13.OptionChainRequest\x1a\x14.OptionChainResponse\x12S\n\x16GetSymbolReferenceData\x12\x1b.SymbolReferenceDataRequest\x1a\x1c.SymbolReferenceDataResponse\x12\x32\n\x0bGetTickData\x12\x10.TickDataRequest\x1a\x11.TickDataResponse\x12S\n\x16GetOptionsAndGreekData\x12\x1b.OptionsAndGreekDataRequest\x1a\x1c.OptionsAndGreekDataResponse\x12>\n\x0fGetSecurityData\x12\x14.SecurityDataRequest\x1a\x15.SecurityDataResponse\x12k\n\x1eGetOptionSymbolFromDescription\x12#.OptionSymbolFromDescriptionRequest\x1a$.OptionSymbolFromDescriptionResponse\x12k\n\x1eGetDescriptionFromOptionSymbol\x12#.DescriptionFromOptionSymbolRequest\x1a$.DescriptionFromOptionSymbolResponse\x12M\n\x14SubscribeLevel1Ticks\x12\x18.Level1MarketDataRequest\x1a\x19.Level1MarketDataResponse0\x01\x12V\n\x15UnSubscribeLevel1Data\x12\x1d.UnSubscribeLevel1DataRequest\x1a\x1e.UnSubscribeLevel1DataResponse\x12M\n\x14SubscribeLevel2Ticks\x12\x18.Level2MarketDataRequest\x1a\x19.Level2MarketDataResponse0\x01\x12V\n\x15UnSubscribeLevel2Data\x12\x1d.UnSubscribeLevel2DataRequest\x1a\x1e.UnSubscribeLevel2DataResponse\x12\x35\n\nAddSymbols\x12\x12.AddSymbolsRequest\x1a\x13.AddSymbolsResponse\x12>\n\rRemoveSymbols\x12\x15.RemoveSymbolsRequest\x1a\x16.RemoveSymbolsResponse\x12\\\n\x19GetSymbolsFromCompanyName\x12\x1e.SymbolsFromCompanyNameRequest\x1a\x1f.SymbolsFromCompanyNameResponse\x12n\n\x1fGetSymbolFromAlternateSymbology\x12$.SymbolFromAlternateSymbologyRequest\x1a%.SymbolFromAlternateSymbologyResponse\x12P\n\x13GetLevel1MarketData\x12\x18.Level1MarketDataRequest\x1a\x1f.Level1MarketDataRecordResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'market_data_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LEVEL1MARKETDATARESPONSE_EXTENDEDFIELDSENTRY._options = None
  _LEVEL1MARKETDATARESPONSE_EXTENDEDFIELDSENTRY._serialized_options = b'8\001'
  _UNSUBSCRIBELEVEL1DATARESPONSE_OPTIONALFIELDSENTRY._options = None
  _UNSUBSCRIBELEVEL1DATARESPONSE_OPTIONALFIELDSENTRY._serialized_options = b'8\001'
  _ADDSYMBOLSRESPONSE_OPTIONALFIELDSENTRY._options = None
  _ADDSYMBOLSRESPONSE_OPTIONALFIELDSENTRY._serialized_options = b'8\001'
  _REMOVESYMBOLSRESPONSE_OPTIONALFIELDSENTRY._options = None
  _REMOVESYMBOLSRESPONSE_OPTIONALFIELDSENTRY._serialized_options = b'8\001'
  _UNSUBSCRIBELEVEL2DATARESPONSE_OPTIONALFIELDSENTRY._options = None
  _UNSUBSCRIBELEVEL2DATARESPONSE_OPTIONALFIELDSENTRY._serialized_options = b'8\001'
  _LEVEL1MARKETDATARECORD_EXTENDEDFIELDSENTRY._options = None
  _LEVEL1MARKETDATARECORD_EXTENDEDFIELDSENTRY._serialized_options = b'8\001'
  _OPTIONTYPES._serialized_start=135
  _OPTIONTYPES._serialized_end=219
  _OPTIONTYPES_OPTIONS._serialized_start=191
  _OPTIONTYPES_OPTIONS._serialized_end=219
  _INTERVAL._serialized_start=221
  _INTERVAL._serialized_end=324
  _INTERVAL_OPTIONS._serialized_start=279
  _INTERVAL_OPTIONS._serialized_end=324
  _TICKTYPES._serialized_start=327
  _TICKTYPES._serialized_end=518
  _TICKTYPES_TICKS._serialized_start=379
  _TICKTYPES_TICKS._serialized_end=518
  _COMMONBARSFIELDS._serialized_start=521
  _COMMONBARSFIELDS._serialized_end=709
  _DAILYWEEKLYMONTHLYBARSREQUEST._serialized_start=712
  _DAILYWEEKLYMONTHLYBARSREQUEST._serialized_end=980
  _DAILYWEEKLYMONTHLYBARSRESPONSE._serialized_start=983
  _DAILYWEEKLYMONTHLYBARSRESPONSE._serialized_end=1120
  _INTRADAYBARSREQUEST._serialized_start=1123
  _INTRADAYBARSREQUEST._serialized_end=1457
  _INTRADAYBARSRESPONSE._serialized_start=1459
  _INTRADAYBARSRESPONSE._serialized_end=1580
  _OPTIONSYMBOLFROMDESCRIPTIONREQUEST._serialized_start=1583
  _OPTIONSYMBOLFROMDESCRIPTIONREQUEST._serialized_end=1727
  _OPTIONSYMBOLFROMDESCRIPTIONRESPONSE._serialized_start=1729
  _OPTIONSYMBOLFROMDESCRIPTIONRESPONSE._serialized_end=1831
  _DESCRIPTIONFROMOPTIONSYMBOLREQUEST._serialized_start=1833
  _DESCRIPTIONFROMOPTIONSYMBOLREQUEST._serialized_end=1904
  _DESCRIPTIONFROMOPTIONSYMBOLRESPONSE._serialized_start=1907
  _DESCRIPTIONFROMOPTIONSYMBOLRESPONSE._serialized_end=2082
  _LEVEL1MARKETDATAREQUEST._serialized_start=2084
  _LEVEL1MARKETDATAREQUEST._serialized_end=2207
  _LEVEL1MARKETDATARESPONSE._serialized_start=2210
  _LEVEL1MARKETDATARESPONSE._serialized_end=3017
  _LEVEL1MARKETDATARESPONSE_EXTENDEDFIELDSENTRY._serialized_start=2964
  _LEVEL1MARKETDATARESPONSE_EXTENDEDFIELDSENTRY._serialized_end=3017
  _UNSUBSCRIBELEVEL1DATAREQUEST._serialized_start=3019
  _UNSUBSCRIBELEVEL1DATAREQUEST._serialized_end=3068
  _UNSUBSCRIBELEVEL1DATARESPONSE._serialized_start=3071
  _UNSUBSCRIBELEVEL1DATARESPONSE._serialized_end=3257
  _UNSUBSCRIBELEVEL1DATARESPONSE_OPTIONALFIELDSENTRY._serialized_start=3204
  _UNSUBSCRIBELEVEL1DATARESPONSE_OPTIONALFIELDSENTRY._serialized_end=3257
  _ADDSYMBOLSREQUEST._serialized_start=3259
  _ADDSYMBOLSREQUEST._serialized_end=3339
  _ADDSYMBOLSRESPONSE._serialized_start=3342
  _ADDSYMBOLSRESPONSE._serialized_end=3506
  _ADDSYMBOLSRESPONSE_OPTIONALFIELDSENTRY._serialized_start=3204
  _ADDSYMBOLSRESPONSE_OPTIONALFIELDSENTRY._serialized_end=3257
  _REMOVESYMBOLSREQUEST._serialized_start=3508
  _REMOVESYMBOLSREQUEST._serialized_end=3591
  _REMOVESYMBOLSRESPONSE._serialized_start=3594
  _REMOVESYMBOLSRESPONSE._serialized_end=3764
  _REMOVESYMBOLSRESPONSE_OPTIONALFIELDSENTRY._serialized_start=3204
  _REMOVESYMBOLSRESPONSE_OPTIONALFIELDSENTRY._serialized_end=3257
  _LEVEL2MARKETDATAREQUEST._serialized_start=3767
  _LEVEL2MARKETDATAREQUEST._serialized_end=3931
  _LEVEL2MARKETDATARESPONSE._serialized_start=3934
  _LEVEL2MARKETDATARESPONSE._serialized_end=4710
  _UNSUBSCRIBELEVEL2DATAREQUEST._serialized_start=4712
  _UNSUBSCRIBELEVEL2DATAREQUEST._serialized_end=4761
  _UNSUBSCRIBELEVEL2DATARESPONSE._serialized_start=4764
  _UNSUBSCRIBELEVEL2DATARESPONSE._serialized_end=4950
  _UNSUBSCRIBELEVEL2DATARESPONSE_OPTIONALFIELDSENTRY._serialized_start=3204
  _UNSUBSCRIBELEVEL2DATARESPONSE_OPTIONALFIELDSENTRY._serialized_end=3257
  _OPTIONCHAINREQUEST._serialized_start=4952
  _OPTIONCHAINREQUEST._serialized_end=5059
  _QUOTECHAINRESPONSE._serialized_start=5062
  _QUOTECHAINRESPONSE._serialized_end=5364
  _OPTIONCHAINRESPONSE._serialized_start=5366
  _OPTIONCHAINRESPONSE._serialized_end=5477
  _SYMBOLREFERENCEDATAREQUEST._serialized_start=5479
  _SYMBOLREFERENCEDATAREQUEST._serialized_end=5542
  _SYMINFORESPONSE._serialized_start=5545
  _SYMINFORESPONSE._serialized_end=5743
  _SYMBOLREFERENCEDATARESPONSE._serialized_start=5745
  _SYMBOLREFERENCEDATARESPONSE._serialized_end=5862
  _TICKDATAREQUEST._serialized_start=5865
  _TICKDATAREQUEST._serialized_end=6162
  _TICKSRESPONSE._serialized_start=6165
  _TICKSRESPONSE._serialized_end=6379
  _TICKDATARESPONSE._serialized_start=6381
  _TICKDATARESPONSE._serialized_end=6482
  _OPTIONSANDGREEKDATAREQUEST._serialized_start=6484
  _OPTIONSANDGREEKDATAREQUEST._serialized_end=6581
  _OPTIONCALCULATIONRESPONSE._serialized_start=6584
  _OPTIONCALCULATIONRESPONSE._serialized_end=7824
  _OPTIONSANDGREEKDATARESPONSE._serialized_start=7826
  _OPTIONSANDGREEKDATARESPONSE._serialized_end=7953
  _SECURITYDATAREQUEST._serialized_start=7955
  _SECURITYDATAREQUEST._serialized_end=8011
  _SECURITYDATA._serialized_start=8014
  _SECURITYDATA._serialized_end=10173
  _SECURITYDATARESPONSE._serialized_start=10175
  _SECURITYDATARESPONSE._serialized_end=10287
  _SYMBOLDATA._serialized_start=10290
  _SYMBOLDATA._serialized_end=10653
  _SYMBOLSFROMCOMPANYNAMEREQUEST._serialized_start=10655
  _SYMBOLSFROMCOMPANYNAMEREQUEST._serialized_end=10726
  _SYMBOLSFROMCOMPANYNAMERESPONSE._serialized_start=10728
  _SYMBOLSFROMCOMPANYNAMERESPONSE._serialized_end=10846
  _ALTERNATESYMBOLOGY._serialized_start=10849
  _ALTERNATESYMBOLOGY._serialized_end=10985
  _ALTERNATESYMBOLOGY_SYMBOLOGY._serialized_start=10924
  _ALTERNATESYMBOLOGY_SYMBOLOGY._serialized_end=10985
  _SYMBOLFROMALTERNATESYMBOLOGYREQUEST._serialized_start=10987
  _SYMBOLFROMALTERNATESYMBOLOGYREQUEST._serialized_end=11100
  _SYMBOLFROMALTERNATESYMBOLOGYRESPONSE._serialized_start=11102
  _SYMBOLFROMALTERNATESYMBOLOGYRESPONSE._serialized_end=11226
  _LEVEL1MARKETDATARECORD._serialized_start=11229
  _LEVEL1MARKETDATARECORD._serialized_end=11983
  _LEVEL1MARKETDATARECORD_EXTENDEDFIELDSENTRY._serialized_start=2964
  _LEVEL1MARKETDATARECORD_EXTENDEDFIELDSENTRY._serialized_end=3017
  _LEVEL1MARKETDATARECORDRESPONSE._serialized_start=11985
  _LEVEL1MARKETDATARECORDRESPONSE._serialized_end=12111
  _MARKETDATASERVICE._serialized_start=12114
  _MARKETDATASERVICE._serialized_end=13609
# @@protoc_insertion_point(module_scope)