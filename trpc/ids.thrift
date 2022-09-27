include "exceptions.thrift"

service IdsService {
    i64 getId(
        1:string target
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie
    )

    bool exists(
        1:string target
    ) throws (
        2:exceptions.InternalException ie
    )

    i64 reset(
        1:string target
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie
    )

    i64 reset_to(
        1:string target,
        2:i64 value
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.InternalException ie
    )
}
