from app import app, db
from flask import request, jsonify
from app.models.DataDosen import DataDosen
from flask_jwt_extended import jwt_required


@app.route("/data-dosen", methods=["POST"])
def create_data_dosen():
    nip = request.json["nip"]
    nama_lengkap = request.json["nama_lengkap"]
    prodi_id = request.json["prodi_id"]

    new_datadosen = DataDosen(nip=nip, nama_lengkap=nama_lengkap, prodi_id=prodi_id)
    db.session.add(new_datadosen)
    db.session.commit()

    return jsonify({"message": "Data Dosen berhasil ditambahkan"})


@app.route("/data-dosen", methods=["GET"])
@jwt_required()
def get_data_dosens():
    datadosen = DataDosen.query.all()
    print(datadosen)
    datadosen_list = []
    for dosen in datadosen:
        datadosen_list.append(
            {
                "nip": dosen.nip,
                "nama_lengkap": dosen.nama_lengkap,
                "prodi_id": dosen.prodi_id,
            }
        )
    return jsonify(datadosen_list)


@app.route("/data-dosen/<nip>", methods=["GET"])
@jwt_required()
def get_data_dosen_by_nip(nip):
    datadosen = DataDosen.query.get_or_404(nip)
    return jsonify(
        {
            "nip": datadosen.nip,
            "nama_lengkap": datadosen.nama_lengkap,
            "prodi_id": datadosen.prodi_id,
        }
    )


@app.route("/data-dosen/<nip>", methods=["PUT", "DELETE"])
def put_delete_data_dosen(nip):
    datadosen = DataDosen.query.get_or_404(nip)

    if request.method == "PUT":
        datadosen.nip = request.json["nip"]
        datadosen.nama_lengkap = request.json["nama_lengkap"]
        datadosen.prodi_id = request.json["prodi_id"]
        db.session.commit()
        return jsonify({"message": "Data Dosen berhasil diperbarui"})

    if request.method == "DELETE":
        db.session.delete(datadosen)
        db.session.commit()
        return jsonify({"message": "Data Dosen berhasil dihapus"})
