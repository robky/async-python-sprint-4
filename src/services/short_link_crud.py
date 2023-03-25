from models.short_link_model import Link as LinkModel
from models.short_link_model import Transfer as TransferModel
from schemas.short_link_schema import (LinkCreate, LinkUpdate, TransferCreate,
                                       TransferUpdate)
from services.base_services import RepositoryDB


class RepositoryLink(RepositoryDB[LinkModel, LinkCreate, LinkUpdate]):
    pass


class RepositoryTransfer(
    RepositoryDB[TransferModel, TransferCreate, TransferUpdate]
):
    pass


link_crud = RepositoryLink(LinkModel)
transfer_crud = RepositoryTransfer(TransferModel)
