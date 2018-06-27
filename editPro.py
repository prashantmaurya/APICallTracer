

def get_package_name():
	pfile = open("package_name")
	package_name = pfile.read()
	package_name = package_name[:-1]
	package_name = "L"+package_name
	package_name = package_name.replace('.','/')
	pfile.close()
	return package_name

def edit_ProSmali(p):

	li = ".class public "+p+"/Pro;\n"
	rest = '''.super Ljava/lang/Object;
.source "Pro.java"


# static fields
.field private static final TAG:Ljava/lang/String; = "Prashant"


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 9
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

'''
	with open("Pro.smali", "a") as myfile:
		myfile.write(li)
		myfile.write(rest)
	myfile.close()
def appendForApi(key,i):
	methodName = "logCurrentAPI"+str(i)
	newMethod = '''.method public static {methodName}()V
    .locals 5

    .prologue
    const/4 v3, 0x1

    .line 12
    new-instance v2, Ljava/lang/Exception;

    invoke-direct {{v2}}, Ljava/lang/Exception;-><init>()V

    invoke-virtual {{v2}}, Ljava/lang/Exception;->getStackTrace()[Ljava/lang/StackTraceElement;

    move-result-object v2

    aget-object v2, v2, v3

    invoke-virtual {{v2}}, Ljava/lang/StackTraceElement;->getClassName()Ljava/lang/String;

    move-result-object v0

    .line 13
    .local v0, "className":Ljava/lang/String;
    new-instance v2, Ljava/lang/Exception;

    invoke-direct {{v2}}, Ljava/lang/Exception;-><init>()V

    invoke-virtual {{v2}}, Ljava/lang/Exception;->getStackTrace()[Ljava/lang/StackTraceElement;

    move-result-object v2

    aget-object v2, v2, v3

    invoke-virtual {{v2}}, Ljava/lang/StackTraceElement;->getMethodName()Ljava/lang/String;

    move-result-object v1

    .line 14
    .local v1, "methodName":Ljava/lang/String;
    const-string v2, "Prashant"

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {{v3}}, Ljava/lang/StringBuilder;-><init>()V

    const-string v4, " "

    invoke-virtual {{v3, v4}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {{v3, v0}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, ";->"

    invoke-virtual {{v3, v4}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {{v3, v1}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    const-string v4, "();->{key}"

    invoke-virtual {{v3, v4}}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {{v3}}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-static {{v2, v3}}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I

    .line 16
    return-void
	.end method \n'''.format(methodName=methodName,key = key)
	with open("Pro.smali", "a") as myfile:
		myfile.write(newMethod)
	myfile.close()

with open("Pro.smali", "w") as myfile:
		myfile.write("")
myfile.close()

p= get_package_name()
edit_ProSmali(p)
i=0
default_api = open("default_api")
for api_num,key in enumerate(default_api,1):
		key = key[:-1]
		i=i+1
		appendForApi(key,i)
	