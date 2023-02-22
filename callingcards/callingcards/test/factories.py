import factory


class ChrMapFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = 'callingcards.ChrMap'
	
	uploader = factory.SubFactory('callingcards.users.test.factories.UserFactory')
	uploadDate = factory.Faker('date_time')
	modified = factory.Faker('date_time')
	refseq = 'NC_001133.9'
	igenome = 'I'
	ensembl = 'I'
	ucsc = 'chrI'
	mitra = 'NC_001133'
	numbered = 1
	chr = 'chr1'
	seqlength = 230218
