from rest_framework import serializers
    

class BankFundAccountSerializer(serializers.Serializer):
    ifsc = serializers.CharField(max_length=16)
    bank_name = serializers.CharField(max_length=32, read_only=True)
    name = serializers.CharField(max_length=120)
    account_number = serializers.CharField(max_length=16)


class VPAAccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=120, read_only=True)
    handle = serializers.CharField(max_length=60, read_only=True)
    address = serializers.CharField(max_length=120)

class FundAccountSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, read_only=True)
    account_type = serializers.CharField()
    vpa = VPAAccountSerializer(required=False)
    contact_id = serializers.CharField(max_length=30)
    bank_account = BankFundAccountSerializer(required=False)

    def validate(self, data):
        errors = {}

        match data['account_type']:
            
            case 'vpa':
                if not data.get('vpa'):
                    errors['vpa'] = 'You have to provide `vpa` payload when account_type is of `vpa`'
                
                if data.get('bank_account'):
                    errors['bank_account'] = 'Invalid payload `bank_account` for account type `vpa`'

            case 'bank_account':
                if not data.get('bank_account'):
                    errors['bank_account'] = 'You have to provide `bank_account` payload when account_type is of `bank_account`'

                if data.get('vpa'):
                    errors['vpa'] = 'Invalid payload `vpa` for account type `bank_account`'
            case _:
                errors['account_type'] = 'Invalid account type'
            
        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        from wallet.razorpay import razorpay
        
        result, response, *other = razorpay.create_fund_account(validated_data)
        if not result:
            raise serializers.ValidationError('Failed to save instance')

        return response



