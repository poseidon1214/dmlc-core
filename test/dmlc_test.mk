TEST=test/logging_test test/filesys_test test/dataiter_test\
	test/iostream_test test/recordio_test test/split_read_test\
	test/stream_read_test test/split_test test/libsvm_parser_test

test/logging_test: test/logging_test.cc
test/filesys_test: test/filesys_test.cc src/io/*.h libdmlc.a
test/dataiter_test: test/dataiter_test.cc  libdmlc.a
test/iostream_test: test/iostream_test.cc libdmlc.a
test/recordio_test: test/recordio_test.cc libdmlc.a
test/split_read_test: test/split_read_test.cc libdmlc.a
test/stream_read_test: test/stream_read_test.cc libdmlc.a
test/split_test: test/split_test.cc libdmlc.a
test/libsvm_parser_test: test/libsvm_parser_test.cc libdmlc.a

$(TEST) :
	$(CXX) $(CFLAGS) -o $@ $(filter %.cpp %.o %.c %.cc %.a,  $^) $(LDFLAGS)
