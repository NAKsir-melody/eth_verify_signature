pragma solidity ^0.4.10;

contract verify_signature {
	event ReturnSigner(
		address signer
	);

	function verify_signature() {
	}

	function get_signer(bytes32 _message, uint8 _v, bytes32 _r, bytes32 _s) returns (address) {
		address signer = ecrecover(_message, _v, _r, _s);
		ReturnSigner(signer);
		return signer;
	}
}
