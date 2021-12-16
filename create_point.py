def create_point():
    try:
        data = request.get_json()
        path_id = data.pop('path_id')

        data_address = {
            'street': data['street'],
            'number': data['number'],
            'city': data['city'].title(),
            'state': data['state'].title(),
            'country': data['country'].title(),
            'postal_code': data['postal_code'],
            'coordenadas': data['coordenadas']
        }
        
        keys_data = list(data.keys())
        for key in keys_data:
            if key=='street' or key =='number' or key=='city' or key=='state' or key=='country' or key=='postal_code' or key=='coordenadas':
                data.pop(key)
            
        AddressModel.validate(**data_address)
        address = create(data_address, AddressModel, '')
        AddressModel.query.filter(AddressModel.street==address.street, AddressModel.number==address.number).first()
            
        data['address_id'] = address.id
            
        PointModel.validate(**data)
        point = create(data, PointModel, '')

        path = PathModel.query.get(path_id)
        path.points.append(point)
            
        current_app.db.session.commit()

        if keys_data.count('initial_date') > 0:
            point.initial_date = point.initial_date.strftime("%d/%m/%Y")
        if keys_data.count('end_date') > 0:
            point.initial_date = point.end_date.strftime("%d/%m/%Y")

        return jsonify(point), 201

    except KeyError as err:
        return {'error': {'Verify key':str(err)}}, 400

    except NotStringError as err:
        return jsonify({'error': str(err)}), 400

    except WrongKeysError as err:
        return jsonify({'error': err.message}), 400

    except NotIntegerError as err:
        return jsonify({'error': str(err)}), 400

    except sqlalchemy.exc.DataError:
        return jsonify({'error': 'Invalid date format! It must be dd/mm/yyyy.'}), 400