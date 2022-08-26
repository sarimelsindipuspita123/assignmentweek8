from flask import Flask, request

from sendDataMongoDB import buildData, getLatestData, getTime, sendData, getData, updateData, deleteData, buildLocation


app = Flask(__name__)


@app.route('/kirim', methods = ['GET', 'POST'])
def sendFunc():
    if request.method == 'POST':
        id_transaksi = request.args.get('id_transaksi')
        kecepatan = request.args.get('kecepatan')
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')

        try:
            kecepatan = float(kecepatan)
            id_transaksi = int(id_transaksi)
            latitude = float(latitude)
            longitude = float(longitude)

        except:
            return '400'

        cmpr = getData({'id_transaksi': id_transaksi})

        if cmpr:

            return 'id_transaksi already exist, use /modify instead'

        loc = buildLocation(latitude, longitude)
        waktu = getTime()
        dta = buildData(id_transaksi, kecepatan, loc, waktu)

        sendData(dta)

        return f'Success! Posted data:\n {dta}'

    if request.method == 'GET':
        return 'Only for POST request!'


@app.route('/look', methods = ['GET', 'POST'])
def showFunc():
    if request.method == 'POST':
        id_transaksi = request.args.get('id_transaksi')

        try:
            id_transaksi = int(id_transaksi)

        except:
            return '400'

        dta = getData({'id_transaksi': id_transaksi})

        if dta is None:
            return f'No data with id_transaksi {id_transaksi} found in the database!'

        return f'Showing data with id_transaksi {id_transaksi}:\n {dta}'

    if request.method == 'GET':

        dta = getLatestData()

        if dta is None:
            return f'No data was found in the database!'

        return f'Latest data found in the database:\n{dta}'

@app.route('/edit', methods = ['GET','POST'])
def modifyFunc():
    if request.method == 'POST':
        id_transaksi = request.args.get('id_transaksi')
        kecepatan = request.args.get('kecepatan')
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')

        try:
            kecepatan = float(kecepatan)
            id_transaksi = int(id_transaksi)
            latitude = float(latitude)
            longitude = float(longitude)

        except:
            return '400'

        cmpr = getData({'id_transaksi': id_transaksi})
        if cmpr is None:
            return f'No data with id_transaksi {id_transaksi} found in the database!'

        old = getData({'id_transaksi': id_transaksi})

        if old is None:
            return f'No data with id_transaksi {id_transaksi} found in the database!'

        loc = buildLocation(latitude, longitude)
        waktu = getTime()
        dta = buildData(id_transaksi, kecepatan, loc, waktu)

        updateData(old, dta)
        new = getData({'id_transaksi': id_transaksi})

        return f'Succes! Data with id_transaksi {id_transaksi} has been modified!\n Old data: \n {old} \n New data: \n {new}'

    if request.method == 'GET':
        return 'Only for POST request!'


@app.route('/hapus', methods = ['GET', 'POST'])
def deleteFunc():
    if request.method == 'POST':
        id_transaksi = request.args.get('id_transaksi')

        try:
            id_transaksi = int(id_transaksi)

        except:
            return '400'

        dta = getData({'id_transaksi': id_transaksi})

        if dta is None:
            return f'No data with id_transaksi {id_transaksi} found in the database!'

        deleteData({'id_transaksi': id_transaksi})

        return f'Success! Data with id_transaksi {id_transaksi} has been deleted!\n Deleted data: \n {dta}'

    if request.method == 'GET':
        return 'Only for POST request!'


if __name__ == '__main__':
    app.run(debug=True, port= 5000)
